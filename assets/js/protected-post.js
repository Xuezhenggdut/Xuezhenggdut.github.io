(function () {
  function decodeBase64(value) {
    var binary = atob(value);
    var bytes = new Uint8Array(binary.length);
    for (var i = 0; i < binary.length; i += 1) {
      bytes[i] = binary.charCodeAt(i);
    }
    return bytes;
  }

  function escapeHtml(value) {
    return value
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function renderMarkdown(markdown) {
    if (window.marked && typeof window.marked.parse === 'function') {
      return window.marked.parse(markdown);
    }
    return '<pre>' + escapeHtml(markdown) + '</pre>';
  }

  async function deriveKey(password, salt) {
    var encodedPassword = new TextEncoder().encode(password);
    var keyMaterial = await crypto.subtle.importKey(
      'raw',
      encodedPassword,
      'PBKDF2',
      false,
      ['deriveKey']
    );

    return crypto.subtle.deriveKey(
      {
        name: 'PBKDF2',
        salt: salt,
        iterations: 250000,
        hash: 'SHA-256'
      },
      keyMaterial,
      { name: 'AES-GCM', length: 256 },
      false,
      ['decrypt']
    );
  }

  async function decryptPost(payload, password) {
    var salt = decodeBase64(payload.salt);
    var iv = decodeBase64(payload.iv);
    var ciphertext = decodeBase64(payload.ciphertext);
    var key = await deriveKey(password, salt);
    var plaintext = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: iv },
      key,
      ciphertext
    );
    return new TextDecoder().decode(plaintext);
  }

  function setMessage(element, text) {
    element.textContent = text || '';
  }

  document.addEventListener('DOMContentLoaded', function () {
    var root = document.querySelector('[data-protected-post]');
    if (!root) {
      return;
    }

    var payloadNode = root.querySelector('[data-protected-payload]');
    var form = root.querySelector('[data-protected-form]');
    var input = root.querySelector('[data-protected-password]');
    var message = root.querySelector('[data-protected-message]');
    var content = root.querySelector('[data-protected-content]');

    if (!window.crypto || !window.crypto.subtle) {
      setMessage(message, 'This browser does not support Web Crypto. Please use a modern browser.');
      return;
    }

    var payload;
    try {
      payload = JSON.parse(JSON.parse(payloadNode.textContent));
    } catch (error) {
      setMessage(message, 'Protected content is not configured correctly.');
      return;
    }

    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      var password = input.value;
      if (!password) {
        setMessage(message, 'Please enter the password.');
        return;
      }

      setMessage(message, 'Unlocking...');
      try {
        var markdown = await decryptPost(payload, password);
        content.innerHTML = renderMarkdown(markdown);
        content.hidden = false;
        form.hidden = true;
        setMessage(message, '');
      } catch (error) {
        setMessage(message, 'Incorrect password.');
      }
    });
  });
}());
