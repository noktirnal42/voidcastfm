<script>
	import { formatFreq } from '../lib/frequency.js';

	let { connected, onPlay } = $props();

  let selectedFile = $state(null);
  let freq = $state(100000000);
  let mode = $state('fm');
  let isDragging = $state(false);

  function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) selectedFile = file;
  }

  function handleDrop(e) {
    e.preventDefault();
    isDragging = false;
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('audio/')) {
      selectedFile = file;
    }
  }

  function handleDragOver(e) {
    e.preventDefault();
    isDragging = true;
  }

  function handleDragLeave() {
    isDragging = false;
  }

  function handlePlay() {
    if (selectedFile) {
		onPlay?.({ file: selectedFile, freq, mode });
    }
  }
</script>

<div class="panel file-panel">
  <div class="panel-header">
    <span class="panel-icon">🎵</span>
    <span class="panel-title">FILE PLAYER</span>
  </div>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
  class="drop-zone"
  class:dragging={isDragging}
  ondrop={handleDrop}
  ondragover={handleDragOver}
  ondragleave={handleDragLeave}
  role="region"
  aria-label="Audio file drop zone"
>
    {#if selectedFile}
      <div class="file-info">
        <span class="file-icon">🎶</span>
        <span class="file-name">{selectedFile.name}</span>
        <span class="file-size">{(selectedFile.size / 1024).toFixed(0)} KB</span>
      </div>
    {:else}
      <div class="drop-prompt">
        <span class="drop-icon">📂</span>
        <span>Drop audio file or</span>
        <label class="browse-btn">
          browse
          <input type="file" accept="audio/*" onchange={handleFileSelect} class="hidden" />
        </label>
      </div>
    {/if}
  </div>

  <div class="file-controls">
    <div class="freq-row">
      <span class="field-label">FREQ</span>
      <input type="number" class="freq-input" bind:value={freq} min="50000" max="1500000000" step="100000" />
      <span class="freq-readout">{formatFreq(freq)}</span>
    </div>
    <div class="mode-row">
      <span class="field-label">MODE</span>
      <select bind:value={mode} class="mode-select">
        <option value="fm">FM</option>
        <option value="am">AM</option>
        <option value="ssb">SSB</option>
      </select>
    </div>
  </div>

  <button
    class="play-btn"
    onclick={handlePlay}
    disabled={!connected || !selectedFile}
  >
    ▶ PLAY FILE
  </button>
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

  .drop-zone {
    border: 2px dashed rgba(0, 245, 255, 0.15);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
    margin-bottom: 12px;
  }

  .drop-zone.dragging {
    border-color: rgba(0, 245, 255, 0.5);
    background: rgba(0, 245, 255, 0.05);
  }

  .drop-prompt {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    font-size: 11px;
    color: rgba(224, 230, 240, 0.5);
  }

  .drop-icon { font-size: 16px; }

  .browse-btn {
    color: #00f5ff;
    cursor: pointer;
    text-decoration: underline;
  }

  .hidden { display: none; }

  .file-info {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
  }

  .file-icon { font-size: 18px; }

  .file-name {
    color: #e0e6f0;
    font-weight: 600;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .file-size {
    color: rgba(0, 245, 255, 0.4);
    font-size: 10px;
    margin-left: auto;
  }

  .file-controls {
    display: flex;
    gap: 8px;
    margin-bottom: 10px;
  }

  .freq-row, .mode-row {
    flex: 1;
  }

  .field-label {
    display: block;
    font-size: 9px;
    letter-spacing: 0.18em;
    color: rgba(0, 245, 255, 0.4);
    margin-bottom: 4px;
    text-transform: uppercase;
  }

  .freq-input, .mode-select {
    width: 100%;
    background: rgba(0, 245, 255, 0.04);
    border: 1px solid rgba(0, 245, 255, 0.1);
    border-radius: 6px;
    padding: 6px 8px;
    color: #e0e6f0;
    font-family: inherit;
    font-size: 11px;
    outline: none;
  }

  .freq-readout {
    font-size: 9px;
    color: rgba(0, 245, 255, 0.4);
  }

  .play-btn {
    width: 100%;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid rgba(139, 92, 246, 0.3);
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.12), rgba(0, 200, 255, 0.06));
    color: #c4b5fd;
    font-family: inherit;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.15em;
    cursor: pointer;
    transition: all 0.25s ease;
  }

  .play-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.22), rgba(0, 200, 255, 0.12));
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.15);
  }

  .play-btn:disabled {
    opacity: 0.25;
    cursor: not-allowed;
  }
</style>
