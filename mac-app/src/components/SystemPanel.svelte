<script>
let { sysInfo, connected } = $props();

  let cpuTemp = $derived(sysInfo.cpu_temp || 0);
  let cpuLoad = $derived(sysInfo.cpu_load || 0);
  let memInfo = $derived(sysInfo.memory || {});
  let diskInfo = $derived(sysInfo.disk || {});

  function tempColor(temp) {
    if (temp < 45) return '#00f5ff';
    if (temp < 60) return '#f5c842';
    if (temp < 75) return '#ff8c00';
    return '#ff3c3c';
  }

  function tempGrade(temp) {
    if (temp < 45) return 'COOL';
    if (temp < 60) return 'WARM';
    if (temp < 75) return 'HOT';
    return 'CRIT';
  }
</script>

<div class="panel system-panel">
  <div class="panel-header">
    <span class="panel-icon">🖥️</span>
    <span class="panel-title">PI SYSTEM</span>
    <span class="hostname">{sysInfo.hostname || 'pi0'}</span>
  </div>

  <!-- CPU Temperature -->
  <div class="stat-block">
    <div class="stat-row">
      <span class="stat-name">CPU TEMP</span>
      <span class="stat-value" style="color: {tempColor(cpuTemp)}">{cpuTemp}°C</span>
    </div>
    <div class="stat-bar-track">
      <div
        class="stat-bar-fill temp-bar"
        style="width: {Math.min(100, (cpuTemp / 85) * 100)}%; background: {tempColor(cpuTemp)}"
      ></div>
    </div>
    <span class="stat-grade" style="color: {tempColor(cpuTemp)}">{tempGrade(cpuTemp)}</span>
  </div>

  <!-- CPU Load -->
  <div class="stat-block">
    <div class="stat-row">
      <span class="stat-name">CPU LOAD</span>
      <span class="stat-value">{cpuLoad.toFixed(2)}</span>
    </div>
    <div class="stat-bar-track">
      <div class="stat-bar-fill" style="width: {Math.min(100, cpuLoad * 25)}%; background: #8b5cf6"></div>
    </div>
  </div>

  <!-- Memory -->
  <div class="stat-block">
    <div class="stat-row">
      <span class="stat-name">MEMORY</span>
      <span class="stat-value">{memInfo.used_mb || 0}/{memInfo.total_mb || 0} MB</span>
    </div>
    <div class="stat-bar-track">
      <div class="stat-bar-fill" style="width: {memInfo.percent || 0}%; background: #00f5ff"></div>
    </div>
    <span class="stat-detail">{memInfo.percent || 0}%</span>
  </div>

  <!-- Disk -->
  <div class="stat-block">
    <div class="stat-row">
      <span class="stat-name">DISK</span>
      <span class="stat-value">{diskInfo.free_mb || 0} MB free</span>
    </div>
    <div class="stat-bar-track">
      <div class="stat-bar-fill" style="width: {diskInfo.percent || 0}%; background: #c4b5fd"></div>
    </div>
    <span class="stat-detail">{diskInfo.percent || 0}%</span>
  </div>

  <!-- IP -->
  <div class="ip-row">
    <span class="field-label">IP</span>
    <span class="ip-addr">{sysInfo.ip || '—'}</span>
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

  .hostname {
    margin-left: auto;
    font-size: 10px;
    color: rgba(0, 245, 255, 0.35);
    letter-spacing: 0.1em;
  }

  .stat-block {
    margin-bottom: 12px;
    position: relative;
  }

  .stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
  }

  .stat-name {
    font-size: 9px;
    letter-spacing: 0.15em;
    color: rgba(224, 230, 240, 0.4);
  }

  .stat-value {
    font-size: 12px;
    font-weight: 600;
    color: #e0e6f0;
  }

  .stat-bar-track {
    height: 4px;
    background: rgba(0, 245, 255, 0.06);
    border-radius: 2px;
    overflow: hidden;
  }

  .stat-bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.5s ease;
  }

  .stat-grade {
    position: absolute;
    right: 0;
    top: 0;
    font-size: 8px;
    letter-spacing: 0.1em;
    opacity: 0.6;
  }

  .stat-detail {
    font-size: 9px;
    color: rgba(0, 245, 255, 0.3);
  }

  .ip-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid rgba(0, 245, 255, 0.06);
  }

  .field-label {
    font-size: 9px;
    letter-spacing: 0.18em;
    color: rgba(0, 245, 255, 0.4);
  }

  .ip-addr {
    font-size: 11px;
    color: #e0e6f0;
    font-weight: 600;
  }
</style>
