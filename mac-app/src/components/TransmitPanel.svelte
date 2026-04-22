<script>
	import { MODES, formatFreq, parseFreq, getBandForFreq, antennaLength } from '../lib/frequency.js';

	let { connected, txStatus, onStart, onStop } = $props();

  let freq = $state(434000000);  // Default ISM band
  let mode = $state('fm');
  let ppm = $state(0);
  let showAdvanced = $state(false);
  let rdsPS = $state('');
  let rdsRT = $state('');
  let freqInput = $state('434.000');

  let band = $derived(getBandForFreq(freq));
  let antLen = $derived(antennaLength(freq));
  let freqDisplay = $derived(formatFreq(freq));

  function updateFreqFromInput() {
    const hz = parseFreq(freqInput);
    if (hz && hz > 0 && hz < 1500000000) {
      freq = hz;
    }
  }

  function handleStart() {
    const opts = { ppm, rds_ps: mode === 'fm' && rdsPS ? rdsPS : null, rds_rt: mode === 'fm' && rdsRT ? rdsRT : null };
		onStart?.({ freq, mode, opts });
  }

  function handleStop() {
		onStop?.();
  }

  // Quick frequency presets
  const presets = [
    { label: 'FM 97.3', freq: 97300000 },
    { label: '2m', freq: 144200000 },
    { label: 'ISM 434', freq: 434000000 },
    { label: '70cm', freq: 432100000 },
    { label: '10m', freq: 28500000 },
    { label: '40m', freq: 7150000 },
  ];
</script>

<div class="panel transmit-panel">
  <div class="panel-header">
    <span class="panel-icon">⚡</span>
    <span class="panel-title">TRANSMIT</span>
  </div>

  <!-- Frequency Control -->
  <div class="freq-section">
    <span class="field-label">FREQUENCY</span>
    <div class="freq-input-row">
      <input
        type="text"
        class="freq-input"
        bind:value={freqInput}
	onchange={updateFreqFromInput}
	onkeydown={e => e.key === 'Enter' && updateFreqFromInput()}
      />
      <span class="freq-display">{freqDisplay}</span>
    </div>
    <input
      type="range"
      class="freq-slider"
      min="50000"
      max="1500000000"
      step="10000"
      bind:value={freq}
	oninput={() => { freqInput = (freq / 1e6).toFixed(3); }}
    />
    {#if band}
      <div class="band-badge">{band.label}</div>
      <div class="antenna-info">λ/4 = {antLen.toFixed(2)}m</div>
    {/if}
  </div>

  <!-- Mode Selector -->
  <div class="mode-section">
    <span class="field-label">MODE</span>
    <div class="mode-grid">
      {#each MODES as m}
        <button
          class="mode-btn"
          class:active={mode === m.id}
		onclick={() => mode = m.id}
          disabled={!connected}
          title={m.description}
        >
          <span class="mode-icon">{m.icon}</span>
          <span class="mode-label">{m.label}</span>
        </button>
      {/each}
    </div>
  </div>

  <!-- Quick Presets -->
  <div class="presets-section">
  <span class="field-label">PRESETS</span>
  <div class="preset-row">
    {#each presets as p}
      <button class="preset-btn" onclick={() => { freq = p.freq; freqInput = (p.freq / 1e6).toFixed(3); }}>
          {p.label}
        </button>
      {/each}
    </div>
  </div>

  <!-- RDS Options (FM only) -->
  {#if mode === 'fm'}
    <div class="rds-section">
      <span class="field-label">RDS</span>
      <input type="text" class="text-input" placeholder="Station Name (8 chars)" bind:value={rdsPS} maxlength={8} />
      <input type="text" class="text-input" placeholder="Radio Text (64 chars)" bind:value={rdsRT} maxlength={64} />
    </div>
  {/if}

  <!-- Advanced -->
  <button class="toggle-advanced" onclick={() => showAdvanced = !showAdvanced}>
    ADVANCED {showAdvanced ? '▾' : '▸'}
  </button>
  {#if showAdvanced}
    <div class="advanced-section">
      <span class="field-label">PPM CORRECTION</span>
      <input type="number" class="text-input" bind:value={ppm} min="-100" max="100" step="1" />
    </div>
  {/if}

  <!-- Action Buttons -->
  <div class="action-row">
  <button
    class="btn btn-start"
    onclick={handleStart}
    disabled={!connected || txStatus.is_running}
  >
      <span class="btn-icon">▶</span> START
    </button>
  <button
    class="btn btn-stop"
    onclick={handleStop}
    disabled={!connected || !txStatus.is_running}
  >
      <span class="btn-icon">■</span> STOP
    </button>
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
    margin-bottom: 16px;
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

  .field-label {
    display: block;
    font-size: 9px;
    letter-spacing: 0.18em;
    color: rgba(0, 245, 255, 0.4);
    margin-bottom: 6px;
    text-transform: uppercase;
  }

  /* ─── Frequency ────────────────────────────── */
  .freq-section { margin-bottom: 16px; }

  .freq-input-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
  }

  .freq-input {
    flex: 1;
    background: rgba(0, 245, 255, 0.05);
    border: 1px solid rgba(0, 245, 255, 0.15);
    border-radius: 8px;
    padding: 8px 12px;
    color: #00f5ff;
    font-family: 'SF Mono', monospace;
    font-size: 16px;
    font-weight: 600;
    outline: none;
    transition: all 0.2s ease;
  }

  .freq-input:focus {
    border-color: rgba(0, 245, 255, 0.4);
    box-shadow: 0 0 16px rgba(0, 245, 255, 0.1);
  }

  .freq-display {
    font-size: 11px;
    color: rgba(139, 92, 246, 0.8);
    white-space: nowrap;
  }

  .freq-slider {
    width: 100%;
    height: 4px;
    -webkit-appearance: none;
    appearance: none;
    background: rgba(0, 245, 255, 0.1);
    border-radius: 2px;
    outline: none;
  }

  .freq-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #00f5ff;
    box-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
    cursor: pointer;
  }

  .band-badge {
    display: inline-block;
    margin-top: 6px;
    padding: 2px 8px;
    border-radius: 4px;
    background: rgba(139, 92, 246, 0.15);
    border: 1px solid rgba(139, 92, 246, 0.3);
    font-size: 10px;
    color: #c4b5fd;
    letter-spacing: 0.1em;
  }

  .antenna-info {
    display: inline-block;
    margin-top: 6px;
    margin-left: 8px;
    font-size: 10px;
    color: rgba(0, 245, 255, 0.4);
  }

  /* ─── Mode Grid ────────────────────────────── */
  .mode-section { margin-bottom: 16px; }

  .mode-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }

  .mode-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    padding: 8px 4px;
    border-radius: 10px;
    border: 1px solid rgba(0, 245, 255, 0.08);
    background: rgba(0, 245, 255, 0.03);
    cursor: pointer;
    transition: all 0.2s ease;
    color: rgba(224, 230, 240, 0.6);
  }

  .mode-btn:hover:not(:disabled) {
    background: rgba(0, 245, 255, 0.08);
    border-color: rgba(0, 245, 255, 0.2);
  }

  .mode-btn.active {
    background: rgba(0, 245, 255, 0.12);
    border-color: rgba(0, 245, 255, 0.5);
    color: #00f5ff;
    box-shadow: 0 0 16px rgba(0, 245, 255, 0.1), inset 0 0 20px rgba(0, 245, 255, 0.05);
  }

  .mode-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  .mode-icon { font-size: 16px; }
  .mode-label { font-size: 9px; letter-spacing: 0.1em; font-weight: 600; }

  /* ─── Presets ──────────────────────────────── */
  .presets-section { margin-bottom: 16px; }

  .preset-row {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
  }

  .preset-btn {
    padding: 4px 8px;
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

  /* ─── RDS ──────────────────────────────────── */
  .rds-section { margin-bottom: 12px; }

  .text-input {
    width: 100%;
    background: rgba(0, 245, 255, 0.04);
    border: 1px solid rgba(0, 245, 255, 0.1);
    border-radius: 6px;
    padding: 6px 10px;
    color: #e0e6f0;
    font-family: inherit;
    font-size: 12px;
    outline: none;
    margin-bottom: 6px;
    transition: border-color 0.2s ease;
  }

  .text-input:focus {
    border-color: rgba(0, 245, 255, 0.3);
  }

  /* ─── Advanced ─────────────────────────────── */
  .toggle-advanced {
    background: none;
    border: none;
    color: rgba(0, 245, 255, 0.35);
    font-size: 9px;
    letter-spacing: 0.15em;
    cursor: pointer;
    padding: 4px 0;
    font-family: inherit;
  }

  .toggle-advanced:hover {
    color: rgba(0, 245, 255, 0.6);
  }

  .advanced-section {
    margin: 8px 0;
    padding: 8px;
    background: rgba(0, 245, 255, 0.03);
    border-radius: 8px;
  }

  /* ─── Action Buttons ───────────────────────── */
  .action-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-top: 12px;
  }

  .btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 12px;
    border-radius: 12px;
    border: none;
    font-family: inherit;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.15em;
    cursor: pointer;
    transition: all 0.25s ease;
  }

  .btn:disabled {
    opacity: 0.25;
    cursor: not-allowed;
  }

  .btn-start {
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.15), rgba(0, 200, 255, 0.08));
    border: 1px solid rgba(0, 245, 255, 0.35);
    color: #00f5ff;
  }

  .btn-start:hover:not(:disabled) {
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.25), rgba(0, 200, 255, 0.15));
    box-shadow: 0 0 24px rgba(0, 245, 255, 0.2);
  }

  .btn-stop {
    background: linear-gradient(135deg, rgba(255, 60, 60, 0.12), rgba(255, 0, 128, 0.08));
    border: 1px solid rgba(255, 60, 60, 0.3);
    color: #ff3c3c;
  }

  .btn-stop:hover:not(:disabled) {
    background: linear-gradient(135deg, rgba(255, 60, 60, 0.22), rgba(255, 0, 128, 0.15));
    box-shadow: 0 0 24px rgba(255, 60, 60, 0.15);
  }

  .btn-icon { font-size: 10px; }
</style>
