<script>
  import { onMount, onDestroy } from 'svelte';
  import { api, settings } from './lib/api.js';
  import HeaderBar from './components/HeaderBar.svelte';
  import TransmitPanel from './components/TransmitPanel.svelte';
  import WaveformDisplay from './components/WaveformDisplay.svelte';
  import WaterfallDisplay from './components/WaterfallDisplay.svelte';
  import FilePlayer from './components/FilePlayer.svelte';
  import MicStreamer from './components/MicStreamer.svelte';
  import Soundboard from './components/Soundboard.svelte';
  import SystemAudio from './components/SystemAudio.svelte';
  import SystemPanel from './components/SystemPanel.svelte';
  import ConnectionIndicator from './components/ConnectionIndicator.svelte';
  import Settings from './components/Settings.svelte';

  // ─── State ────────────────────────────────────────
  let connected = $state(false);
  let txStatus = $state({ is_running: false, mode: 'idle', freq: 0, elapsed: 0 });
  let sysInfo = $state({ cpu_temp: 0, cpu_load: 0, memory: {}, disk: {} });
  let showSettings = $state(false);

  onMount(() => {
    api.onConnectionChange = (state) => { connected = state; };
    api.onStatusUpdate = (data) => {
      if (data.tx) txStatus = data.tx;
      if (data.system) sysInfo = data.system;
    };
    api.connectWS();
  });

  onDestroy(() => {
    api.disconnectWS();
  });
</script>

<div class="voidcast-app">
    <div class="bg-mesh"></div>
    <div class="scan-line"></div>

    <HeaderBar {connected} {txStatus} onOpenSettings={() => showSettings = true} />

    <main class="main-grid">
      <div class="panel-col-left">
        <TransmitPanel {connected} {txStatus} onStart={(d) => api.startTX(d.freq, d.mode, d.opts)} onStop={() => api.stopTX()} />
        <FilePlayer {connected} onPlay={(d) => api.playFile(d.file, d.freq, d.mode)} />
        <MicStreamer {connected} {txStatus} />
        <SystemAudio {connected} {txStatus} />
        <Soundboard {connected} {txStatus} />
      </div>

      <div class="panel-col-center">
        <WaterfallDisplay {txStatus} />
        <WaveformDisplay {txStatus} />
      </div>

      <div class="panel-col-right">
        <SystemPanel {sysInfo} {connected} />
        <ConnectionIndicator {connected} />
      </div>
    </main>

    <footer class="status-bar">
      <span class="status-label">VoidCastFM v1.0</span>
      <span class="status-dot" class:active={txStatus.is_running}></span>
      <span class="status-mode">{txStatus.is_running ? `${txStatus.mode?.toUpperCase()} @ ${(txStatus.freq / 1e6).toFixed(3)} MHz` : 'STANDBY'}</span>
      <span class="status-elapsed">{txStatus.is_running ? `${txStatus.elapsed}s` : ''}</span>
    </footer>

    {#if showSettings}
      <Settings onClose={() => showSettings = false} />
    {/if}
  </div>

<style>
  :global(*) {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  :global(body) {
    background: #08080f;
    color: #e0e6f0;
    font-family: 'SF Mono', 'JetBrains Mono', 'Fira Code', monospace;
    overflow: hidden;
    height: 100vh;
    -webkit-font-smoothing: antialiased;
  }

  :global(#app) {
    height: 100vh;
  }

  .voidcast-app {
    height: 100vh;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
  }

  /* ─── Mesh Gradient Background ────────────────── */
  .bg-mesh {
    position: fixed;
    inset: 0;
    z-index: 0;
    background:
      radial-gradient(ellipse at 15% 20%, rgba(0, 245, 255, 0.06) 0%, transparent 50%),
      radial-gradient(ellipse at 85% 30%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
      radial-gradient(ellipse at 50% 80%, rgba(255, 0, 128, 0.04) 0%, transparent 50%),
      radial-gradient(ellipse at 70% 60%, rgba(0, 200, 255, 0.03) 0%, transparent 40%);
    animation: meshShift 20s ease-in-out infinite alternate;
  }

  @keyframes meshShift {
    0% { filter: hue-rotate(0deg); }
    50% { filter: hue-rotate(15deg); }
    100% { filter: hue-rotate(-10deg); }
  }

  /* ─── Scan Line Effect ────────────────────────── */
  .scan-line {
    position: fixed;
    inset: 0;
    z-index: 1;
    pointer-events: none;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0, 245, 255, 0.015) 2px,
      rgba(0, 245, 255, 0.015) 4px
    );
  }

  /* ─── Main Grid ───────────────────────────────── */
  .main-grid {
    flex: 1;
    display: grid;
    grid-template-columns: 340px 1fr 280px;
    gap: 16px;
    padding: 12px 16px;
    position: relative;
    z-index: 2;
    overflow: hidden;
  }

  .panel-col-left,
  .panel-col-center,
  .panel-col-right {
    display: flex;
    flex-direction: column;
    gap: 12px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(0, 245, 255, 0.3) transparent;
  }

  /* ─── Status Bar ──────────────────────────────── */
  .status-bar {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 6px 16px;
    background: rgba(8, 8, 15, 0.9);
    border-top: 1px solid rgba(0, 245, 255, 0.15);
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }

  .status-label {
    color: rgba(0, 245, 255, 0.6);
  }

  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(255, 60, 60, 0.6);
    box-shadow: 0 0 6px rgba(255, 60, 60, 0.3);
    transition: all 0.3s ease;
  }

  .status-dot.active {
    background: #00f5ff;
    box-shadow: 0 0 12px rgba(0, 245, 255, 0.6), 0 0 30px rgba(0, 245, 255, 0.2);
    animation: pulse 1.5s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }

  .status-mode {
    color: #e0e6f0;
    font-weight: 600;
  }

  .status-elapsed {
    color: rgba(0, 245, 255, 0.7);
    margin-left: auto;
  }
</style>
