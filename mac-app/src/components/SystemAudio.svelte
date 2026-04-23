<script>
  import { api, settings } from '../lib/api.js';
  import { formatFreq } from '../lib/frequency.js';

  let { connected, txStatus } = $props();

  let isStreaming = $state(false);
  let freq = $state(100000000);
  let mode = $state('fm');
  let port = $state(5001); // Different port from mic streamer
  let streamCommand = $state('');
  let ffplayCommand = $state('');

  // Auto-update commands when params change
  $effect(() => {
    const piHost = settings.get('piHost') || 'pi0.local';
    // Mac command to capture system audio and send to Pi
    // Uses BlackHole (virtual audio driver) or Soundflower
    streamCommand = `ffmpeg -f avfoundation -i ":0" -f s16le -ar 44100 -ac 1 udp://${piHost}:${port}`;

    // Alternative using Soundflower/BlackHole with loopback
    ffplayCommand = `ffplay -nodisp -ar 44100 -ac 1 -f s16le udp://${piHost}:${port}`;
  });

  const PRESETS = [
    { label: 'FM 97.3', freq: 97300000 },
    { label: 'FM 104.5', freq: 104500000 },
    { label: 'ISM 434', freq: 434000000 },
  ];

  async function startSystemAudio() {
    if (!connected) return;
    try {
      const result = await api.startAudioStream(freq, mode, port);
      if (result.status === 'audio_listening') {
        isStreaming = true;
      }
    } catch (e) {
      console.error('System audio start failed:', e);
    }
  }

  async function stopSystemAudio() {
    try {
      await api.stopAudioStream();
      isStreaming = false;
    } catch (e) {
      console.error('System audio stop failed:', e);
    }
  }
</script>

<div class="panel system-audio-panel">
  <div class="panel-header">
    <span class="panel-icon">🔊</span>
    <span class="panel-title">SYSTEM AUDIO</span>
    {#if isStreaming}
      <span class="stream-badge">LIVE</span>
    {/if}
  </div>

  <div class="description">
    <span>Stream Mac system audio (music, videos, browser) over RF</span>
  </div>

  <!-- Frequency Controls -->
  <div class="freq-section">
    <span class="field-label">TRANSMIT FREQUENCY</span>
    <div class="freq-row">
      <input
        type="number"
        class="freq-input"
        bind:value={freq}
        min="50000"
        max="1500000000"
        step="100000"
        disabled={isStreaming}
      />
      <span class="freq-display">{formatFreq(freq)}</span>
    </div>
    <div class="presets">
      {#each PRESETS as p}
        <button
          class="preset-btn"
          onclick={() => { freq = p.freq; }}
          disabled={isStreaming}
        >
          {p.label}
        </button>
      {/each}
    </div>
  </div>

  <!-- Mode Selector -->
  <div class="mode-section">
    <span class="field-label">MODE</span>
    <select bind:value={mode} class="mode-select" disabled={isStreaming}>
      <option value="fm">FM</option>
      <option value="am">AM</option>
      <option value="ssb">SSB</option>
    </select>
  </div>

  <!-- Stream Info -->
  {#if isStreaming}
    <div class="info-section">
      <div class="info-row">
        <span class="field-label">STREAM COMMAND (Run on Mac)</span>
        <code class="cmd-block">{streamCommand}</code>
      </div>
      <div class="info-row">
        <span class="field-label">SETUP REQUIREMENTS</span>
        <ul class="setup-list">
          <li>Install BlackHole: <code>brew install blackhole-2ch</code></li>
          <li>Set system output to "BlackHole 2ch"</li>
          <li>Run the command above in Terminal</li>
        </ul>
      </div>
    </div>
  {/if}

  <!-- Action Buttons -->
  <div class="action-row">
    {#if !isStreaming}
      <button
        class="btn btn-go"
        onclick={startSystemAudio}
        disabled={!connected || txStatus.is_running}
      >
        <span class="btn-icon">🔊</span>
        STREAM SYSTEM AUDIO
      </button>
    {:else}
      <button
        class="btn btn-stop"
        onclick={stopSystemAudio}
      >
        <span class="btn-icon">■</span>
        STOP STREAM
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

  .panel:hover {
    border-color: rgba(0, 245, 255, 0.2);
  }

  .panel-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
  }

  .panel-icon {
    font-size: 14px;
  }

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
    margin-left: auto;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
  }

  .description {
    font-size: 10px;
    color: rgba(224, 230, 240, 0.5);
    margin-bottom: 12px;
    padding: 8px;
    background: rgba(0, 245, 255, 0.03);
    border-radius: 6px;
    border: 1px solid rgba(0, 245, 255, 0.05);
  }

  .field-label {
    display: block;
    font-size: 9px;
    letter-spacing: 0.18em;
    color: rgba(0, 245, 255, 0.4);
    margin-bottom: 4px;
    text-transform: uppercase;
  }

  /* Frequency Section */
  .freq-section {
    margin-bottom: 10px;
  }

  .freq-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
  }

  .freq-input {
    flex: 1;
    background: rgba(0, 245, 255, 0.05);
    border: 1px solid rgba(0, 245, 255, 0.15);
    border-radius: 8px;
    padding: 8px 12px;
    color: #00f5ff;
    font-family: 'SF Mono', monospace;
    font-size: 14px;
    font-weight: 600;
    outline: none;
    transition: all 0.2s ease;
  }

  .freq-input:focus:not(:disabled) {
    border-color: rgba(0, 245, 255, 0.4);
    box-shadow: 0 0 16px rgba(0, 245, 255, 0.1);
  }

  .freq-input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .freq-display {
    font-size: 10px;
    color: rgba(139, 92, 246, 0.8);
    white-space: nowrap;
  }

  .presets {
    display: flex;
    gap: 4px;
    flex-wrap: wrap;
  }

  .preset-btn {
    padding: 3px 8px;
    border-radius: 6px;
    border: 1px solid rgba(139, 92, 246, 0.15);
    background: rgba(139, 92, 246, 0.06);
    color: rgba(196, 181, 253, 0.7);
    font-size: 9px;
    letter-spacing: 0.05em;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
  }

  .preset-btn:hover:not(:disabled) {
    background: rgba(139, 92, 246, 0.15);
    border-color: rgba(139, 92, 246, 0.35);
    color: #c4b5fd;
  }

  .preset-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  /* Mode Section */
  .mode-section {
    margin-bottom: 12px;
  }

  .mode-select {
    width: 100%;
    background: rgba(0, 245, 255, 0.04);
    border: 1px solid rgba(0, 245, 255, 0.1);
    border-radius: 8px;
    padding: 8px 12px;
    color: #e0e6f0;
    font-family: inherit;
    font-size: 12px;
    outline: none;
    cursor: pointer;
  }

  .mode-select:focus {
    border-color: rgba(0, 245, 255, 0.3);
  }

  .mode-select:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Info Section */
  .info-section {
    margin-bottom: 12px;
  }

  .info-row {
    margin-bottom: 10px;
  }

  .cmd-block {
    display: block;
    padding: 8px;
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(0, 245, 255, 0.1);
    border-radius: 6px;
    font-family: 'SF Mono', monospace;
    font-size: 9px;
    color: rgba(0, 245, 255, 0.7);
    word-break: break-all;
    margin-top: 4px;
  }

  .setup-list {
    margin: 0;
    padding-left: 16px;
    font-size: 10px;
    color: rgba(224, 230, 240, 0.6);
  }

  .setup-list li {
    margin-bottom: 4px;
  }

  .setup-list code {
    background: rgba(139, 92, 246, 0.1);
    padding: 2px 4px;
    border-radius: 3px;
    color: #c4b5fd;
  }

  /* Action Buttons */
  .action-row {
    display: flex;
  }

  .btn {
    flex: 1;
    padding: 12px;
    border-radius: 12px;
    border: none;
    font-family: inherit;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    cursor: pointer;
    transition: all 0.25s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
  }

  .btn:disabled {
    opacity: 0.25;
    cursor: not-allowed;
  }

  .btn-go {
    background: linear-gradient(
      135deg,
      rgba(139, 92, 246, 0.15),
      rgba(0, 200, 255, 0.08)
    );
    border: 1px solid rgba(139, 92, 246, 0.3);
    color: #c4b5fd;
  }

  .btn-go:hover:not(:disabled) {
    background: linear-gradient(
      135deg,
      rgba(139, 92, 246, 0.25),
      rgba(0, 200, 255, 0.15)
    );
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.15);
  }

  .btn-stop {
    background: linear-gradient(
      135deg,
      rgba(255, 60, 60, 0.15),
      rgba(255, 0, 128, 0.08)
    );
    border: 1px solid rgba(255, 60, 60, 0.3);
    color: #ff3c3c;
  }

  .btn-stop:hover {
    background: linear-gradient(
      135deg,
      rgba(255, 60, 60, 0.25),
      rgba(255, 0, 128, 0.15)
    );
    box-shadow: 0 0 20px rgba(255, 60, 60, 0.15);
  }

  .btn-icon {
    font-size: 12px;
  }
</style>
