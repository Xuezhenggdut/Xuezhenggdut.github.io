---
title: 'Protected Post Example'
date: 2099-01-01
permalink: /posts/protected-example/
layout: protected-post
published: false
tags:
  - Private
encrypted_content: '{"version":1,"kdf":"PBKDF2-HMAC-SHA256","iterations":250000,"cipher":"AES-256-GCM","salt":"replace-me","iv":"replace-me","ciphertext":"replace-me"}'
---

Usage:

1. Write the private markdown body in a local file that is not committed, for example `private-note.md`.
2. Run `node scripts/encrypt-protected-post.js private-note.md -o encrypted.json`.
3. Copy the single-line JSON from `encrypted.json` into `encrypted_content` above.
4. Keep `layout: protected-post` and do not paste the private markdown body into this file.
5. Delete `private-note.md` and `encrypted.json`, or keep them outside the repository.
