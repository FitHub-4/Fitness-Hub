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
    input.classList.add('chat-input');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      onSend(input.value);
    });

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
      <form class="chat-form" autocomplete="off">
        <input class="chat-input" type="text" placeholder="Ask anything..." maxlength="600" required>
        <button type="submit" class="chat-form__send" aria-label="Send">\u2191</button>
      </form>
      <p class="chat-foot">Informational only \u2014 not medical advice.</p>
    `;
    document.body.appendChild(fab);
    document.body.appendChild(panel);

    panel.querySelector('.chat-panel__close').addEventListener('click', closeWidget);
    const form = panel.querySelector('.chat-form');
    const input = panel.querySelector('.chat-input');
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
