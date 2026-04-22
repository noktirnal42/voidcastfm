<script>
  import { onMount } from 'svelte';
  import { api } from '../lib/api.js';
  import { formatFreq } from '../lib/frequency.js';

  let { connected, txStatus } = $props();

  let tones = $state([]);
  let loading = $state(false);
  let freq = $state(100000000); // Default FM broadcast
  let mode = $state('fm');

  const TONE_PRESETS = [
    { label: 'FM 97.3', freq: 97300000 },
    { label: 'FM 104.5', freq: 104500000 },
    { label: 'ISM 434', freq: 434000000 },
  ];

  onMount(async () => {
    await loadTones();
  });

  async function loadTones() {
    if (!connected) return;
    loading = true;
    try {
      const data = await api.getTones();
      tones = Object.values(data.tones || {});
    } catch (e) {
      console.error('Failed to load tones:', e);
    } finally {
      loading = false;
    }
  }

  async function playTone(tone) {
    if (!connected) return;
    try {
      await api.playTone(tone.id, freq, mode);
    } catch (e) {
      console.error('Failed to play tone:', e);
    }
  }

  async function stopTone() {
    try {
      await api.stopTone();
    } catch (e) {
      console.error('Failed to stop tone:', e);
    }
  }
</script>

<div class="panel soundboard-panel">
  <div class="panel-header">
    <span class="panel-icon">🚨</span>
    <span class="panel-title">SOUNDBOARD</span>
    {#if loading}
      <span class="loading-badge">⟳</span>
    {/if}
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
      />
      <span class="freq-display">{formatFreq(freq)}</span>
    </div>
    <div class="freq-presets">
      {#each TONE_PRESETS as p}
        <button
          class="preset-btn"
          onclick={() => { freq = p.freq; }}
          class:active={freq === p.freq}
        >
          {p.label}
        </button>
      {/each}
    </div>
  </div>

  <!-- Mode Selector -->
  <div class="mode-section">
    <span class="field-label">MODE</span>
    <div class="mode-row">
      {#each ['fm', 'am'] as m}
        <button
          class="mode-btn"
          class:active={mode === m}
          onclick={() => { mode = m; }}
        >
          {m.toUpperCase()}
        </button>
      {/each}
    </div>
  </div>

  <!-- Alert Tones Grid -->
  <div class="tones-section">
    <span class="field-label">EMERGENCY ALERTS</span>
    <div class="tones-grid">
      {#each tones as tone}
        <button
          class="tone-card"
          style="--tone-color: {tone.color || '#00f5ff'}"
          onclick={() => playTone(tone)}
          disabled={!connected || txStatus.is_running}
          class:playing={txStatus.is_running && txStatus.mode?.includes('play')}
        >
          <span class="tone-icon">{tone.icon}</span>
          <span class="tone-name">{tone.name}</span>
          <span class="tone-desc">{tone.description}</span>
          <span class="tone-duration">⏱ {tone.duration}s</span>
        </button>
      {/each}
    </div>
    {#if tones.length === 0 && !loading}
      <div class="empty-state">
        <span>No tones loaded</span>
        <button class="retry-btn" onclick={loadTones} disabled={!connected}>
          Retry
        </button>
      </div>
    {/if}
  </div>

  <!-- Stop Button -->
  {#if txStatus.is_running}
    <button
      class="stop-btn"
      onclick={stopTone}
      disabled={!connected}
    >
      <span class="stop-icon">■</span>
      STOP ALERT
    </button>
  {/if}
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
    margin-bottom: 14px;
  }

  .panel-icon {
    font-size: 16px;
  }

  .panel-title {
    font-size: 11px;
    letter-spacing: 0.2em;
    color: rgba(0, 245, 255, 0.7);
    font-weight: 700;
  }

  .loading-badge {
    font-size: 12px;
    animation: spin 1s linear infinite;
    margin-left: auto;
  }

  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  .field-label {
    display: block;
    font-size: 9px;
    letter-spacing: 0.18em;
    color: rgba(0, 245, 255, 0.4);
    margin-bottom: 6px;
    text-transform: uppercase;
  }

  /* Frequency Section */
  .freq-section {
    margin-bottom: 12px;
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

  .freq-input:focus {
    border-color: rgba(0, 245, 255, 0.4);
    box-shadow: 0 0 16px rgba(0, 245, 255, 0.1);
  }

  .freq-display {
    font-size: 10px;
    color: rgba(139, 92, 246, 0.8);
    white-space: nowrap;
  }

  .freq-presets {
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

  .preset-btn:hover {
    background: rgba(139, 92, 246, 0.15);
    border-color: rgba(139, 92, 246, 0.35);
    color: #c4b5fd;
  }

  .preset-btn.active {
    background: rgba(0, 245, 255, 0.12);
    border-color: rgba(0, 245, 255, 0.4);
    color: #00f5ff;
  }

  /* Mode Section */
  .mode-section {
    margin-bottom: 14px;
  }

  .mode-row {
    display: flex;
    gap: 8px;
  }

  .mode-btn {
    flex: 1;
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid rgba(0, 245, 255, 0.1);
    background: rgba(0, 245, 255, 0.04);
    color: rgba(224, 230, 240, 0.5);
    font-family: inherit;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.15em;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .mode-btn:hover {
    border-color: rgba(0, 245, 255, 0.25);
    color: rgba(224, 230, 240, 0.8);
  }

  .mode-btn.active {
    background: rgba(0, 245, 255, 0.1);
    border-color: rgba(0, 245, 255, 0.4);
    color: #00f5ff;
  }

  /* Tones Section */
  .tones-section {
    margin-bottom: 12px;
  }

  .tones-grid {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .tone-card {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid rgba(255, 60, 60, 0.15);
    background: linear-gradient(
      135deg,
      rgba(255, 60, 60, 0.06),
      rgba(12, 12, 20, 0.7)
    );
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    text-align: left;
    font-family: inherit;
  }

  .tone-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 12px;
    padding: 1px;
    background: linear-gradient(
      135deg,
      var(--tone-color, #00f5ff),
      transparent 60%
    );
    -webkit-mask:
      linear-gradient(#fff 0 0) content-box,
      linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    opacity: 0.3;
    transition: opacity 0.3s ease;
  }

  .tone-card:hover:not(:disabled) {
    border-color: rgba(255, 60, 60, 0.3);
    transform: translateY(-1px);
  }

  .tone-card:hover:not(:disabled)::before {
    opacity: 0.6;
  }

  .tone-card:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .tone-card.playing {
    animation: playing-pulse 1s ease-in-out infinite;
    border-color: var(--tone-color, #00f5ff);
  }

  @keyframes playing-pulse {
    0%, 100% {
      box-shadow: 0 0 0 0 rgba(255, 60, 60, 0.2);
    }
    50% {
      box-shadow: 0 0 20px 4px rgba(255, 60, 60, 0.3);
    }
  }

  .tone-icon {
    font-size: 20px;
    margin-bottom: 2px;
  }

  .tone-name {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #e0e6f0;
  }

  .tone-desc {
    font-size: 9px;
    color: rgba(224, 230, 240, 0.5);
    line-height: 1.3;
  }

  .tone-duration {
    position: absolute;
    top: 8px;
    right: 8px;
    font-size: 9px;
    color: rgba(0, 245, 255, 0.5);
    letter-spacing: 0.05em;
  }

  /* Empty State */
  .empty-state {
    text-align: center;
    padding: 20px;
    color: rgba(224, 230, 240, 0.4);
  }

  .empty-state span {
    display: block;
    font-size: 11px;
    margin-bottom: 8px;
  }

  .retry-btn {
    padding: 6px 12px;
    border-radius: 6px;
    border: 1px solid rgba(0, 245, 255, 0.2);
    background: rgba(0, 245, 255, 0.05);
    color: #00f5ff;
    font-size: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .retry-btn:hover:not(:disabled) {
    background: rgba(0, 245, 255, 0.1);
  }

  /* Stop Button */
  .stop-btn {
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid rgba(255, 60, 60, 0.4);
    background: linear-gradient(
      135deg,
      rgba(255, 60, 60, 0.15),
      rgba(255, 0, 128, 0.08)
    );
    color: #ff3c3c;
    font-family: inherit;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.15em;
    cursor: pointer;
    transition: all 0.25s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }

  .stop-btn:hover:not(:disabled) {
    background: linear-gradient(
      135deg,
      rgba(255, 60, 60, 0.25),
      rgba(255, 0, 128, 0.15)
    );
    box-shadow: 0 0 24px rgba(255, 60, 60, 0.2);
  }

  .stop-icon {
    font-size: 10px;
  }
</style>
