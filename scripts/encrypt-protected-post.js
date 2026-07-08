#!/usr/bin/env node
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

function usage() {
  console.error('Usage: node scripts/encrypt-protected-post.js <input.md> [-o output.json]');
}

function parseArgs(argv) {
  const args = argv.slice(2);
  if (args.length < 1) {
    usage();
    process.exit(1);
  }

  const result = { input: args[0], output: null };
  for (let index = 1; index < args.length; index += 1) {
    if ((args[index] === '-o' || args[index] === '--output') && args[index + 1]) {
      result.output = args[index + 1];
      index += 1;
    } else {
      usage();
      process.exit(1);
    }
  }
  return result;
}

function askHidden(rl, query) {
  return new Promise((resolve) => {
    rl.question(query, (answer) => {
      process.stderr.write('\n');
      resolve(answer);
    });
  });
}

async function readPasswords() {
  if (!process.stdin.isTTY) {
    const lines = fs.readFileSync(0, 'utf8').split(/\r?\n/);
    return [lines[0] || '', lines[1] || ''];
  }

  const rl = readline.createInterface({ input: process.stdin, output: process.stderr });
  const writeToOutput = rl._writeToOutput;
  rl._writeToOutput = function (text) {
    if (rl.stdoutMuted) {
      rl.output.write(text.replace(/./g, '*'));
    } else {
      writeToOutput.call(rl, text);
    }
  };
  rl.stdoutMuted = true;

  const password = await askHidden(rl, 'Password: ');
  const confirm = await askHidden(rl, 'Confirm password: ');
  rl.close();
  return [password, confirm];
}

async function main() {
  const args = parseArgs(process.argv);
  const inputPath = path.resolve(args.input);
  const plaintext = fs.readFileSync(inputPath);

  const [password, confirm] = await readPasswords();
  if (password !== confirm) {
    throw new Error('Passwords do not match.');
  }
  if (!password) {
    throw new Error('Password cannot be empty.');
  }

  const salt = crypto.randomBytes(16);
  const iv = crypto.randomBytes(12);
  const key = crypto.pbkdf2Sync(password, salt, 250000, 32, 'sha256');
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const authTag = cipher.getAuthTag();

  const payload = {
    version: 1,
    kdf: 'PBKDF2-HMAC-SHA256',
    iterations: 250000,
    cipher: 'AES-256-GCM',
    salt: salt.toString('base64'),
    iv: iv.toString('base64'),
    ciphertext: Buffer.concat([encrypted, authTag]).toString('base64')
  };

  const output = JSON.stringify(payload);
  if (args.output) {
    fs.writeFileSync(path.resolve(args.output), `${output}\n`, 'utf8');
  } else {
    process.stdout.write(`${output}\n`);
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
