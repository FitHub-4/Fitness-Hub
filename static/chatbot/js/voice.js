(function () {
  'use strict';

  function getCsrfToken() {
    const name = 'csrftoken';
    const parts = document.cookie.split('; ').map(p => p.split('='));
    for (const [k, v] of parts) {
      if (k === name) return decodeURIComponent(v || '');
    }
    return '';
  }

  function initVoice() {
    const btn = document.getElementById('landing-voice-toggle');
    if (!btn) return; // safe no-op if element is absent

    let mediaRecorder = null;
    let stream = null;
    let chunks = [];

    async function startRecording() {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mimeType = MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/mp3';
        mediaRecorder = new MediaRecorder(stream, { mimeType });
        chunks = [];

        mediaRecorder.ondataavailable = (e) => {
          if (e.data && e.data.size) chunks.push(e.data);
        };

        mediaRecorder.onstop = handleStop;
        mediaRecorder.start();
        btn.classList.add('is-recording');
      } catch (err) {
        console.warn('Microphone not available', err);
      }
    }

    async function handleStop() {
      btn.classList.remove('is-recording');
      if (!chunks.length) return;
      const blob = new Blob(chunks, { type: mediaRecorder.mimeType || 'audio/webm' });
      const formData = new FormData();
      formData.append('audio', blob, 'recording.webm');

      const csrf = getCsrfToken();

      try {
        const resp = await fetch('/chatbot/voice/', {
          method: 'POST',
          credentials: 'same-origin',
          headers: {
            'X-CSRFToken': csrf,
            'X-Requested-With': 'XMLHttpRequest',
          },
          body: formData,
        });

        if (!resp.ok) {
          const errJson = await resp.json().catch(() => ({}));
          console.error('Voice request failed', errJson);
          return;
        }

        const audioBlob = await resp.blob();
        const url = URL.createObjectURL(audioBlob);
        const audio = new Audio(url);
        await audio.play().catch(()=>{});
      } catch (err) {
        console.error('Voice fetch error', err);
      } finally {
        if (stream) stream.getTracks().forEach(t => t.stop());
        stream = null;
        mediaRecorder = null;
        chunks = [];
      }
    }

    btn.addEventListener('click', () => {
      if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
      } else {
        startRecording();
        setTimeout(() => {
          if (mediaRecorder && mediaRecorder.state === 'recording') mediaRecorder.stop();
        }, 8000);
      }
    });
  }

  window.fitnessChatVoiceInit = function () {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initVoice);
    } else {
      initVoice();
    }
  };
})();
