<script>
  import { onMount, onDestroy } from 'svelte';

  let { txStatus } = $props();

  let canvas;
  let ctx;
  let animFrame;
  let time = 0;

  onMount(() => {
    ctx = canvas.getContext('2d');
    draw();
  });

  onDestroy(() => {
    if (animFrame) cancelAnimationFrame(animFrame);
  });

  function draw() {
    if (!ctx) return;
    const w = canvas.width = canvas.offsetWidth * 2;
    const h = canvas.height = canvas.offsetHeight * 2;
    ctx.scale(2, 2);
    const rw = w / 2;
    const rh = h / 2;

    // Background
    ctx.fillStyle = 'rgba(8, 8, 15, 0.85)';
    ctx.fillRect(0, 0, rw, rh);

    // Grid lines
    ctx.strokeStyle = 'rgba(0, 245, 255, 0.06)';
    ctx.lineWidth = 0.5;
    for (let y = 0; y < rh; y += 20) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(rw, y); ctx.stroke();
    }
    for (let x = 0; x < rw; x += 20) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, rh); ctx.stroke();
    }

    // Center line
    ctx.strokeStyle = 'rgba(0, 245, 255, 0.12)';
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(0, rh / 2); ctx.lineTo(rw, rh / 2); ctx.stroke();

    time += 0.02;
    const isActive = txStatus.is_running;
    const amplitude = isActive ? 0.35 : 0.05;

    // Primary waveform
    ctx.beginPath();
    ctx.strokeStyle = isActive ? '#00f5ff' : 'rgba(0, 245, 255, 0.25)';
    ctx.lineWidth = isActive ? 2 : 1;
    ctx.shadowColor = '#00f5ff';
    ctx.shadowBlur = isActive ? 12 : 4;

    for (let x = 0; x < rw; x++) {
      const t = x / rw;
      const freq = isActive ? 8 + Math.sin(time * 0.3) * 2 : 3;
      const y = rh / 2 +
        Math.sin(t * Math.PI * freq + time * 3) * rh * amplitude +
        Math.sin(t * Math.PI * freq * 2.7 + time * 1.7) * rh * amplitude * 0.3 +
        Math.sin(t * Math.PI * freq * 0.5 + time * 0.5) * rh * amplitude * 0.2;
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Secondary ghost waveform
    ctx.beginPath();
    ctx.strokeStyle = 'rgba(139, 92, 246, 0.3)';
    ctx.lineWidth = 1;
    ctx.shadowColor = '#8b5cf6';
    ctx.shadowBlur = 6;

    for (let x = 0; x < rw; x++) {
      const t = x / rw;
      const freq = isActive ? 6 + Math.cos(time * 0.4) * 1.5 : 2;
      const y = rh / 2 +
        Math.sin(t * Math.PI * freq + time * 2.3 + 1) * rh * amplitude * 0.6 +
        Math.cos(t * Math.PI * freq * 1.8 + time * 1.2) * rh * amplitude * 0.15;
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    ctx.shadowBlur = 0;

    // Mode label
    if (isActive) {
      ctx.font = '10px "SF Mono", monospace';
      ctx.fillStyle = 'rgba(0, 245, 255, 0.5)';
      ctx.fillText(txStatus.mode?.toUpperCase() || '', 8, 14);
    }

    animFrame = requestAnimationFrame(draw);
  }
</script>

<div class="panel waveform-panel">
  <div class="panel-header">
    <span class="panel-icon">〰️</span>
    <span class="panel-title">WAVEFORM</span>
    {#if txStatus.is_running}
      <span class="live-badge">LIVE</span>
    {/if}
  </div>
  <canvas bind:this={canvas} class="waveform-canvas"></canvas>
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
    margin-bottom: 8px;
  }

  .panel-icon { font-size: 14px; }

  .panel-title {
    font-size: 11px;
    letter-spacing: 0.2em;
    color: rgba(0, 245, 255, 0.7);
    font-weight: 700;
  }

  .live-badge {
    font-size: 9px;
    padding: 2px 8px;
    border-radius: 4px;
    background: rgba(0, 245, 255, 0.12);
    border: 1px solid rgba(0, 245, 255, 0.3);
    color: #00f5ff;
    letter-spacing: 0.12em;
    animation: pulse 1.5s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
  }

  .waveform-canvas {
    width: 100%;
    height: 120px;
    border-radius: 8px;
    display: block;
  }
</style>
