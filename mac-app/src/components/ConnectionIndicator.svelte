<script>
  let { connected } = $props();

  let pingMs = $state(null);
  let interval;

  import { onMount, onDestroy } from 'svelte';
  import { api, settings } from '../lib/api.js';

  onMount(() => {
    interval = setInterval(async () => {
      if (connected) {
        const start = performance.now();
        try {
          // Use the API proxy in dev, direct in production
          const url = api.baseUrl + '/';
          await fetch(url, { method: 'GET', mode: 'no-cors' });
          pingMs = Math.round(performance.now() - start);
        } catch {
          pingMs = null;
        }
      } else {
        pingMs = null;
      }
    }, 3000);
  });

  onDestroy(() => {
    clearInterval(interval);
  });

  function pingColor(ms) {
    if (!ms) return 'rgba(255,60,60,0.6)';
    if (ms < 10) return '#00f5ff';
    if (ms < 50) return '#8b5cf6';
    if (ms < 100) return '#f5c842';
    return '#ff3c3c';
  }
</script>

<div class="panel connection-panel">
  <div class="panel-header">
    <span class="panel-icon">🔗</span>
    <span class="panel-title">LINK</span>
  </div>

  <div class="link-status">
    <div class="link-indicator" class:active={connected}>
      <div class="link-ring" style="--ring-color: {connected ? '#00f5ff' : '#ff3c3c'}">
        <div class="link-core"></div>
      </div>
    </div>

    <div class="link-details">
      <span class="link-state">{connected ? 'CONNECTED' : 'DISCONNECTED'}</span>
      <span class="link-target">
        {settings.get('piHost') ? `${settings.get('piHost')}:${settings.get('piPort')}` : '⚠️ Configure in Settings'}
      </span>
      {#if pingMs !== null}
        <span class="link-ping" style="color: {pingColor(pingMs)}">{pingMs}ms</span>
      {:else}
        <span class="link-ping" style="color: rgba(255,60,60,0.4)">{connected ? '—' : 'Click ⚙️ to configure'}</span>
      {/if}
    </div>
  </div>

  <!-- Signal strength bars -->
  <div class="signal-bars">
    {#each [1,2,3,4,5] as bar}
      <div
        class="signal-bar"
        class:lit={pingMs !== null && (
          bar === 1 ? true :
          bar === 2 ? pingMs < 100 :
          bar === 3 ? pingMs < 50 :
          bar === 4 ? pingMs < 20 :
          pingMs < 10
        )}
      ></div>
    {/each}
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
    margin-bottom: 14px;
  }

  .panel-icon { font-size: 14px; }

  .panel-title {
    font-size: 11px;
    letter-spacing: 0.2em;
    color: rgba(0, 245, 255, 0.7);
    font-weight: 700;
  }

  .link-status {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 12px;
  }

  .link-indicator {
    position: relative;
    width: 40px;
    height: 40px;
  }

  .link-ring {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 2px solid var(--ring-color);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 16px color-mix(in srgb, var(--ring-color) 30%, transparent);
    transition: all 0.4s ease;
  }

  .link-core {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--ring-color);
    box-shadow: 0 0 8px var(--ring-color);
    transition: all 0.4s ease;
  }

  .link-details {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .link-state {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #e0e6f0;
  }

  .link-target {
    font-size: 10px;
    color: rgba(0, 245, 255, 0.4);
  }

  .link-ping {
    font-size: 10px;
    font-weight: 600;
  }

  .signal-bars {
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 24px;
  }

  .signal-bar {
    width: 6px;
    border-radius: 2px;
    background: rgba(0, 245, 255, 0.1);
    transition: all 0.3s ease;
  }

  .signal-bar:nth-child(1) { height: 6px; }
  .signal-bar:nth-child(2) { height: 10px; }
  .signal-bar:nth-child(3) { height: 14px; }
  .signal-bar:nth-child(4) { height: 18px; }
  .signal-bar:nth-child(5) { height: 24px; }

  .signal-bar.lit {
    background: #00f5ff;
    box-shadow: 0 0 6px rgba(0, 245, 255, 0.4);
  }
</style>
