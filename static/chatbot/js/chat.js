(function () {
  'use strict';

  const API_URL = '/chatbot/api/';

  function el(tag, attrs, children) {
    const node = document.createElement(tag);
    if (attrs) {
      for (const k in attrs) {
        if (k === 'className') node.className = attrs[k];
        else if (k === 'dataset') Object.assign(node.dataset, attrs[k]);
        else if (k === 'html') node.innerHTML = attrs[k];
        else if (k.indexOf('on') === 0 && typeof attrs[k] === 'function') {
          node.addEventListener(k.slice(2), attrs[k]);
        } else {
          node.setAttribute(k, attrs[k]);
        }
      }
    }
    if (children) {
      (Array.isArray(children) ? children : [children]).forEach((c) => {
        if (c == null) return;
        node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
      });
    }
    return node;
  }

  function getCookie(name) {
    const parts = document.cookie.split('; ');
    for (const p of parts) {
      const [k, v] = p.split('=');
      if (k === name) return decodeURIComponent(v);
    }
    return '';
  }

  function csrfToken() {
    const fromCookie = getCookie('csrftoken');
    if (fromCookie) return fromCookie;
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') || '' : '';
  }

  function escapeHtml(s) {
    return s
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function bubbleHtml(text) {
    const safe = escapeHtml(text)
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');
    return safe;
  }

  function appendMessage(log, text, role) {
    const avatar = el('div', { className: 'chat-msg__avatar', 'aria-hidden': 'true' },
      role === 'bot' ? '\u2726' : '\u{1F464}'
    );
    const bubble = el('div', { className: 'chat-msg__bubble', html: bubbleHtml(text) });
    const body = el('div', { className: 'chat-msg__body' }, bubble);
    const wrap = el('div', { className: 'chat-msg chat-msg--' + role }, [avatar, body]);
    log.appendChild(wrap);
    log.scrollTop = log.scrollHeight;
    return wrap;
  }

  function attachVoiceInputToSurface(surface) {
    if (!surface) return;
    const voiceBtn = surface.querySelector('.chat-form__voice');
    if (!voiceBtn || voiceBtn.dataset.voiceBound === 'true') return;

    voiceBtn.dataset.voiceBound = 'true';
    let mediaRecorder = null;
    let stream = null;
    let chunks = [];
    let timeoutId = null;

    function resetVoiceUi() {
      if (timeoutId) {
        clearTimeout(timeoutId);
        timeoutId = null;
      }
      voiceBtn.classList.remove('is-recording');
      voiceBtn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15.5a3.5 3.5 0 0 0 3.5-3.5V6a3.5 3.5 0 1 0-7 0v6a3.5 3.5 0 0 0 3.5 3.5Z"/><path d="M7 11.5a1 1 0 0 0-2 0 5.5 5.5 0 0 0 5 5.47V20H8.5a1 1 0 1 0 0 2h7a1 1 0 1 0 0-2H14v-3.03a5.5 5.5 0 0 0 5-5.47 1 1 0 1 0-2 0 3.5 3.5 0 0 1-7 0Z"/></svg>';
      voiceBtn.setAttribute('aria-pressed', 'false');
      voiceBtn.setAttribute('aria-label', 'Speak with voice');
    }

    async function finishRecording() {
      if (timeoutId) {
        clearTimeout(timeoutId);
        timeoutId = null;
      }

      if (!chunks.length) {
        resetVoiceUi();
        return;
      }

      const blob = new Blob(chunks, { type: mediaRecorder && mediaRecorder.mimeType ? mediaRecorder.mimeType : 'audio/webm' });
      const formData = new FormData();
      formData.append('audio', blob, 'voice.webm');

      const log = surface.querySelector('.chat-log');
      const status = el('div', {
        className: 'chat-msg chat-msg--bot',
        html: '<div class="chat-msg__avatar" aria-hidden="true">🎤</div><div class="chat-msg__body"><div class="chat-msg__bubble">Listening…</div></div>',
      });
      if (log) {
        log.appendChild(status);
        log.scrollTop = log.scrollHeight;
      }

      try {
        const response = await fetch('/chatbot/voice/', {
          method: 'POST',
          body: formData,
          credentials: 'same-origin',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken(),
          },
        });

        if (!response.ok) {
          const payload = await response.json().catch(() => ({}));
          throw new Error(payload.error || 'Voice request failed');
        }

        const audioBlob = await response.blob();
        if (audioBlob.size) {
          const audioUrl = URL.createObjectURL(audioBlob);
          const audio = new Audio(audioUrl);
          await audio.play().catch(() => {});
        }

        if (status.parentNode) status.parentNode.removeChild(status);
      } catch (err) {
        if (status.parentNode) status.parentNode.removeChild(status);
        if (log) appendMessage(log, 'Voice input could not be processed right now.', 'bot');
      } finally {
        resetVoiceUi();
        if (stream) {
          stream.getTracks().forEach((track) => track.stop());
          stream = null;
        }
        mediaRecorder = null;
        chunks = [];
      }
    }

    voiceBtn.addEventListener('click', async function () {
      if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        return;
      }

      try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mimeType = MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/mp3';
        mediaRecorder = new MediaRecorder(stream, { mimeType });
        chunks = [];

        mediaRecorder.addEventListener('dataavailable', (event) => {
          if (event.data && event.data.size) chunks.push(event.data);
        });
        mediaRecorder.addEventListener('stop', finishRecording);

        mediaRecorder.start();
        voiceBtn.classList.add('is-recording');
        voiceBtn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15.5a3.5 3.5 0 0 0 3.5-3.5V6a3.5 3.5 0 1 0-7 0v6a3.5 3.5 0 0 0 3.5 3.5Z"/><path d="M7 11.5a1 1 0 0 0-2 0 5.5 5.5 0 0 0 5 5.47V20H8.5a1 1 0 1 0 0 2h7a1 1 0 1 0 0-2H14v-3.03a5.5 5.5 0 0 0 5-5.47 1 1 0 1 0-2 0 3.5 3.5 0 0 1-7 0Z"/></svg>';
        voiceBtn.setAttribute('aria-pressed', 'true');
        voiceBtn.setAttribute('aria-label', 'Listening');
        timeoutId = window.setTimeout(() => {
          if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
          }
        }, 8000);
      } catch (err) {
        const log = surface.querySelector('.chat-log');
        if (log) appendMessage(log, 'Microphone access was denied or is unavailable.', 'bot');
      }
    });
  }

  function onSend(text) {
    text = (text || '').trim();
    if (!text) return;

    const surface = currentSurface();
    if (!surface) return;
    const log = surface.querySelector('.chat-log');
    const form = surface.querySelector('.chat-form');
    const input = surface.querySelector('.chat-input');
    const sendBtn = surface.querySelector('.chat-form__send');

    appendMessage(log, text, 'user');
    if (input) input.value = '';
    if (sendBtn) sendBtn.disabled = true;

    const typing = el('div', {
      className: 'chat-msg chat-msg--bot',
      html: '<div class="chat-msg__avatar" aria-hidden="true">\u2726</div><div class="chat-msg__body"><div class="chat-msg__bubble"><span class="chat-typing"><span></span><span></span><span></span></span></div></div>',
    });
    log.appendChild(typing);
    log.scrollTop = log.scrollHeight;

    fetch(API_URL, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken(),
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: JSON.stringify({ message: text }),
    })
      .then((r) => r.json())
      .then((data) => {
        if (typing.parentNode) typing.parentNode.removeChild(typing);
        appendMessage(log, data.reply || '(no response)', 'bot');
      })
      .catch((err) => {
        if (typing.parentNode) typing.parentNode.removeChild(typing);
        appendMessage(log, '\u26A0\uFE0F Network error \u2014 please try again.', 'bot');
      })
      .finally(() => {
        if (sendBtn) sendBtn.disabled = false;
        if (input) input.focus();
      });
  }

  function currentSurface() {
    const open = document.querySelector('.chat-panel.is-open');
    if (open) return open;
    const page = document.querySelector('.chat-page .chat-card');
    if (page) return page;
    return null;
  }

  function initFullPage() {
    const card = document.querySelector('.chat-page .chat-card');
    if (!card) return;
    const form = card.querySelector('#chat-form');
    const input = card.querySelector('#chat-input');
    const voiceBtn = card.querySelector('#voice-toggle');
    input.classList.add('chat-input');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      onSend(input.value);
    });

    attachVoiceInputToSurface(card);

    const log = card.querySelector('.chat-log');
    if (log) log.scrollTop = log.scrollHeight;
  }

  let widgetBooted = false;

  function buildWidget() {
    if (document.querySelector('.chat-fab')) return;

    const fab = el('button', {
      type: 'button',
      className: 'chat-fab',
      'aria-label': 'Open fitness coach',
      title: 'Ask the coach',
    }, '\u2728');
    fab.addEventListener('click', toggleWidget);

    const panel = el('div', { className: 'chat-panel floating', role: 'dialog', 'aria-label': 'Fitness coach' });
    panel.innerHTML = `
      <div class="chat-header">
        <div class="chat-header__avatar" aria-hidden="true">\u2726</div>
        <span class="chat-header__title">Fitness Coach</span>
        <span class="chat-header__sub">AI-powered</span>
        <button type="button" class="chat-panel__close" aria-label="Close">&times;</button>
      </div>
      <div class="chat-log" role="log" aria-live="polite">
        <div class="chat-msg chat-msg--bot">
          <div class="chat-msg__avatar" aria-hidden="true">\u2726</div>
          <div class="chat-msg__body">
            <div class="chat-msg__bubble">Hey \u2014 ask me for exercises, app help, or nutrition basics.</div>
          </div>
        </div>
      </div>
      <div class="chat-hint">Tap the mic to speak naturally</div>
      <form class="chat-form" autocomplete="off">
        <input class="chat-input" type="text" placeholder="Ask anything..." maxlength="600" required>        <button type="button" class="chat-form__voice" aria-label="Speak with voice"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15.5a3.5 3.5 0 0 0 3.5-3.5V6a3.5 3.5 0 1 0-7 0v6a3.5 3.5 0 0 0 3.5 3.5Z"/><path d="M7 11.5a1 1 0 0 0-2 0 5.5 5.5 0 0 0 5 5.47V20H8.5a1 1 0 1 0 0 2h7a1 1 0 1 0 0-2H14v-3.03a5.5 5.5 0 0 0 5-5.47 1 1 0 1 0-2 0 3.5 3.5 0 0 1-7 0Z"/></svg></button>        <button type="submit" class="chat-form__send" aria-label="Send">\u2191</button>
      </form>
      <p class="chat-foot">Informational only \u2014 not medical advice.</p>
    `;
    document.body.appendChild(fab);
    document.body.appendChild(panel);

    panel.querySelector('.chat-panel__close').addEventListener('click', closeWidget);
    const form = panel.querySelector('.chat-form');
    const input = panel.querySelector('.chat-input');
    attachVoiceInputToSurface(panel);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      onSend(input.value);
    });
    widgetBooted = true;
  }

  function openWidget() {
    buildWidget();
    const p = document.querySelector('.chat-panel');
    p.classList.add('is-open');
    const i = p.querySelector('.chat-input');
    if (i) setTimeout(() => i.focus(), 50);
  }
  function closeWidget() {
    const p = document.querySelector('.chat-panel');
    if (p) p.classList.remove('is-open');
  }
  function toggleWidget() {
    const p = document.querySelector('.chat-panel');
    if (!p) return openWidget();
    if (p.classList.contains('is-open')) closeWidget();
    else openWidget();
  }

  function injectTypingStyles() {
    if (document.getElementById('chat-typing-styles')) return;
    const style = document.createElement('style');
    style.id = 'chat-typing-styles';
    style.textContent = `
      .chat-typing { display: inline-flex; gap: 4px; align-items: center; }
      .chat-typing span {
        width: 6px; height: 6px; border-radius: 50%;
        background: #8895aa;
        display: inline-block;
        animation: typingBlink 1.2s infinite ease-in-out;
      }
      .chat-typing span:nth-child(2) { animation-delay: 0.15s; }
      .chat-typing span:nth-child(3) { animation-delay: 0.3s; }
      @keyframes typingBlink {
        0%, 80%, 100% { opacity: 0.25; transform: translateY(0); }
        40% { opacity: 1; transform: translateY(-2px); }
      }
    `;
    document.head.appendChild(style);
  }

  function boot() {
    injectTypingStyles();
    initFullPage();
    if (!document.querySelector('.chat-page .chat-card')) {
      buildWidget();
    }
    window.__fitnessChat = { open: openWidget, close: closeWidget, send: onSend };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
