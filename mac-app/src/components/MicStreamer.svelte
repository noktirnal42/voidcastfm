<script>
  import { api } from '../lib/api.js';
let { connected, txStatus } = $props();

  let isStreaming = $state(false);
  let freq = $state(100000000);
  let mode = $state('fm');
  let port = $state(5000);

  async function startStream() {
    try {
      const result = await api.startAudioStream(freq, mode, port);
      if (result.status === 'audio_listening') {
        isStreaming = true;
      }
    } catch (e) {
      console.error('Audio stream start failed:', e);
    }
  }

  async function stopStream() {
    try {
      await api.stopAudioStream();
      isStreaming = false;
    } catch (e) {
      console.error('Audio stream stop failed:', e);
    }
  }
</script>

<div class="panel mic-panel">
  <div class="panel-header">
    <span class="panel-icon">🎙️</span>
    <span class="panel-title">LIVE MIC</span>
    {#if isStreaming}
      <span class="stream-badge">STREAMING</span>
    {/if}
  </div>

  <div class="mic-controls">
    <div class="control-row">
      <span class="field-label">FREQ (Hz)</span>
      <input type="number" class="text-input" bind:value={freq} min="50000" max="1500000000" step="100000" disabled={isStreaming} />
    </div>
    <div class="control-row">
      <span class="field-label">MODE</span>
      <select bind:value={mode} class="text-input" disabled={isStreaming}>
        <option value="fm">FM</option>
        <option value="am">AM</option>
        <option value="ssb">SSB</option>
      </select>
    </div>
  </div>

  {#if isStreaming}
    <div class="stream-info">
      <div class="stream-cmd">ffmpeg -f avfoundation -i ":0" -f s16le -ar 44100 -ac 1 udp://192.168.1.25:{port}</div>
    </div>
  {/if}

  <div class="action-row">
    {#if !isStreaming}
      <button class="btn btn-go" onclick={startStream} disabled={!connected || txStatus.is_running}>
        🎙️ GO LIVE
      </button>
    {:else}
      <button class="btn btn-stop-mic" onclick={stopStream}>
        ■ STOP MIC
      </button>
    {/if}
  </div>
</div>

<style>
  .panel {
    background: rgba(12, 12, 20, 0.7);
    backdrop-filter: blur(24px) saturate(150%);
    -webkit-backdrop-filter: blur(24px) saturate(150%);
    border: 1px solid rgba(0, 245, 255, 0.1);
    border-radius: 16px;
    padding: 16px;
    transition: border-color 0.3s ease;
  }

  .panel:hover { border-color: rgba(0, 245, 255, 0.2); }

  .panel-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
  }

  .panel-icon { font-size: 14px; }

  .panel-title {
    font-size: 11px;
    letter-spacing: 0.2em;
    color: rgba(0, 245, 255, 0.7);
    font-weight: 700;
  }

  .stream-badge {
    font-size: 9px;
    padding: 2px 8px;
    border-radius: 4px;
    background: rgba(255, 0, 128, 0.15);
    border: 1px solid rgba(255, 0, 128, 0.3);
    color: #ff0080;
    letter-spacing: 0.1em;
    animation: pulse 1.5s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
  }

  .mic-controls {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 12px;
  }

  .control-row { }

  .field-label {
    display: block;
    font-size: 9px;
    letter-spacing: 0.18em;
    color: rgba(0, 245, 255, 0.4);
    margin-bottom: 4px;
    text-transform: uppercase;
  }

  .text-input {
    width: 100%;
    background: rgba(0, 245, 255, 0.04);
    border: 1px solid rgba(0, 245, 255, 0.1);
    border-radius: 6px;
    padding: 6px 10px;
    color: #e0e6f0;
    font-family: inherit;
    font-size: 11px;
    outline: none;
  }

  .stream-info {
    margin-bottom: 10px;
    padding: 8px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 6px;
    border: 1px solid rgba(0, 245, 255, 0.08);
  }

  .stream-cmd {
    font-family: 'SF Mono', monospace;
    font-size: 9px;
    color: rgba(0, 245, 255, 0.5);
    word-break: break-all;
  }

  .action-row {
    display: flex;
  }

  .btn {
    flex: 1;
    padding: 10px;
    border-radius: 10px;
    border: none;
    font-family: inherit;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    cursor: pointer;
    transition: all 0.25s ease;
  }

  .btn:disabled { opacity: 0.25; cursor: not-allowed; }

  .btn-go {
    background: linear-gradient(135deg, rgba(255, 0, 128, 0.12), rgba(255, 60, 60, 0.08));
    border: 1px solid rgba(255, 0, 128, 0.3);
    color: #ff0080;
  }

  .btn-go:hover:not(:disabled) {
    box-shadow: 0 0 20px rgba(255, 0, 128, 0.15);
  }

  .btn-stop-mic {
    background: linear-gradient(135deg, rgba(255, 60, 60, 0.12), rgba(255, 0, 128, 0.08));
    border: 1px solid rgba(255, 60, 60, 0.3);
    color: #ff3c3c;
  }

  .btn-stop-mic:hover {
    box-shadow: 0 0 20px rgba(255, 60, 60, 0.15);
  }
</style>
