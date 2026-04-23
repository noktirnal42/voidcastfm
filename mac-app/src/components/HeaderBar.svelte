<script>
  let { connected, txStatus, onOpenSettings } = $props();
</script>

<header class="header">
  <div class="logo-section">
    <div class="logo-icon">
      <svg viewBox="0 0 40 40" fill="none">
        <path d="M10 32 L20 8 L30 32" stroke="url(#lg)" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        <line x1="14" y1="24" x2="26" y2="24" stroke="url(#lg)" stroke-width="2" stroke-linecap="round"/>
        <circle cx="20" cy="5" r="2.5" fill="#00f5ff"/>
        <defs>
          <linearGradient id="lg" x1="10" y1="32" x2="30" y2="8">
            <stop offset="0%" stop-color="#8b5cf6"/>
            <stop offset="100%" stop-color="#00f5ff"/>
          </linearGradient>
        </defs>
      </svg>
    </div>
    <div class="title-block">
      <h1 class="title">VoidCast</h1>
      <span class="subtitle">FM</span>
    </div>
  </div>

  <div class="header-actions">
    <button class="settings-btn" onclick={() => onOpenSettings?.()} title="Settings">
      ⚙️
    </button>
    <div class="header-stats">
      <div class="stat-chip" class:live={txStatus.is_running}>
        <span class="chip-dot"></span>
        <span>{txStatus.is_running ? 'TX LIVE' : 'STANDBY'}</span>
      </div>
      <div class="stat-chip conn" class:connected>
        <span class="chip-dot"></span>
        <span>{connected ? 'LINK OK' : 'NO LINK'}</span>
      </div>
    </div>
  </div>
</header>

<style>
  .header {
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    background: rgba(8, 8, 15, 0.85);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border-bottom: 1px solid rgba(0, 245, 255, 0.12);
  }

  .logo-section {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .logo-icon {
    width: 40px;
    height: 40px;
    filter: drop-shadow(0 0 8px rgba(0, 245, 255, 0.3));
  }

  .title-block {
    display: flex;
    flex-direction: column;
    line-height: 1;
  }

  .title {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 0.15em;
    background: linear-gradient(135deg, #00f5ff, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .subtitle {
    font-size: 10px;
    letter-spacing: 0.35em;
    color: rgba(0, 245, 255, 0.5);
    margin-top: 2px;
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .settings-btn {
    background: rgba(0, 245, 255, 0.05);
    border: 1px solid rgba(0, 245, 255, 0.15);
    border-radius: 8px;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .settings-btn:hover {
    background: rgba(0, 245, 255, 0.15);
    border-color: rgba(0, 245, 255, 0.35);
    box-shadow: 0 0 16px rgba(0, 245, 255, 0.2);
  }

  .header-stats {
    display: flex;
    gap: 10px;
  }

  .stat-chip {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    background: rgba(255, 60, 60, 0.12);
    border: 1px solid rgba(255, 60, 60, 0.25);
    font-size: 10px;
    letter-spacing: 0.12em;
    color: rgba(255, 60, 60, 0.8);
    transition: all 0.4s ease;
  }

  .stat-chip.live {
    background: rgba(0, 245, 255, 0.1);
    border-color: rgba(0, 245, 255, 0.35);
    color: #00f5ff;
    box-shadow: 0 0 20px rgba(0, 245, 255, 0.1);
  }

  .stat-chip.conn {
    background: rgba(255, 60, 60, 0.1);
    border-color: rgba(255, 60, 60, 0.2);
    color: rgba(255, 60, 60, 0.7);
  }

  .stat-chip.conn.connected {
    background: rgba(0, 245, 255, 0.06);
    border-color: rgba(0, 245, 255, 0.2);
    color: rgba(0, 245, 255, 0.7);
  }

  .chip-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
    box-shadow: 0 0 6px currentColor;
  }

  .stat-chip.live .chip-dot {
    animation: pulse 1.5s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.7); }
  }
</style>
