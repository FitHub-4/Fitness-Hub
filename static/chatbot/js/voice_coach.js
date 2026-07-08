(function () {
  'use strict';

  const trigger = document.getElementById('mic-toggle');
  if (!trigger) {
    return;
  }

  let mediaRecorder = null;
  let stream = null;
  let chunks = [];
  let recordingTimer = null;
  let isBusy = false;

  function setButtonState(state) {
    trigger.textContent = state;
    trigger.dataset.state = state;
    trigger.classList.toggle('is-recording', state === 'Listening...');
    trigger.classList.toggle('is-processing', state === 'Processing...');
  }

  function stopStream() {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
    }
    stream = null;
  }

  function resetRecorder() {
    if (recordingTimer) {
      window.clearTimeout(recordingTimer);
      recordingTimer = null;
    }
    stopStream();
    mediaRecorder = null;
    chunks = [];
    isBusy = false;
  }

  function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') || '' : '';
  }

  async function sendAudio(blob) {
    const formData = new FormData();
    formData.append('audio', blob, 'voice.webm');

    const response = await fetch('/chatbot/voice/', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'X-CSRFToken': getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: formData,
    });

    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      throw new Error(payload.error || 'Voice request failed.');
    }

    const audioBlob = await response.blob();
    if (!audioBlob.size) {
      throw new Error('The coach returned an empty audio response.');
    }
    return audioBlob;
  }

  async function stopAndProcess() {
    if (!mediaRecorder || mediaRecorder.state !== 'recording') {
      return;
    }

    setButtonState('Processing...');
    isBusy = true;

    try {
      await new Promise((resolve) => {
        mediaRecorder.onstop = () => resolve();
        mediaRecorder.stop();
      });

      const mimeType = mediaRecorder.mimeType || 'audio/webm';
      const blob = new Blob(chunks, { type: mimeType });
      setButtonState('Speaking...');

      const audioBlob = await sendAudio(blob);
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.autoplay = true;
      await audio.play();

      audio.addEventListener('ended', () => URL.revokeObjectURL(audioUrl), { once: true });
      audio.addEventListener('error', () => URL.revokeObjectURL(audioUrl), { once: true });
    } catch (error) {
      console.error('Voice coach error:', error);
      setButtonState('Mic');
    } finally {
      resetRecorder();
      setButtonState('Mic');
    }
  }

  async function startRecording() {
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm';

      mediaRecorder = new MediaRecorder(stream, { mimeType });
      chunks = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size) {
          chunks.push(event.data);
        }
      };

      mediaRecorder.start();
      setButtonState('Listening...');

      recordingTimer = window.setTimeout(() => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
          void stopAndProcess();
        }
      }, 7000);
    } catch (error) {
      console.error('Microphone access error:', error);
      setButtonState('Mic');
      resetRecorder();
    }
  }

  trigger.addEventListener('click', async () => {
    if (isBusy) {
      return;
    }

    if (mediaRecorder && mediaRecorder.state === 'recording') {
      await stopAndProcess();
      return;
    }

    await startRecording();
  });
})();
