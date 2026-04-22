<script>
  import { onMount, onDestroy } from 'svelte';

  let { txStatus } = $props();

  let canvas;
  let ctx;
  let animFrame;
  let time = 0;
  let history = [];  // Waterfall rows

  onMount(() => {
    ctx = canvas.getContext('2d');
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    draw();
  });

  onDestroy(() => {
    if (animFrame) cancelAnimationFrame(animFrame);
    window.removeEventListener('resize', resizeCanvas);
  });

  function resizeCanvas() {
    canvas.width = canvas.offsetWidth * 2;
    canvas.height = canvas.offsetHeight * 2;
  }

  function generateSpectrumRow(width, isActive) {
    const row = new Float32Array(width);
    const center = width / 2;
    const bw = isActive ? 40 + Math.sin(time * 0.5) * 15 : 8;
    const amp = isActive ? 0.8 : 0.15;

    for (let i = 0; i < width; i++) {
      const dist = Math.abs(i - center);
      // Main signal
      let val = Math.exp(-(dist * dist) / (2 * bw * bw)) * amp;
      // Noise floor
      val += (Math.random() * 0.03) * (isActive ? 1.5 : 0.5);
      // Random spikes (interference simulation)
      if (Math.random() < 0.002) val += Math.random() * 0.3;
      row[i] = Math.min(1, val);
    }
    return row;
  }

  function valueToColor(v) {
    // Dark blue → cyan → white heat map
    if (v < 0.1) return [8, 8 + v * 200, 15 + v * 300];
    if (v < 0.3) return [0, 50 + v * 650, 60 + v * 600];
    if (v < 0.6) return [0, v * 400, 200 + v * 90];
    if (v < 0.8) return [v * 300, 200 + v * 55, 255];
    return [200 + v * 55, 240 + v * 15, 255];
  }

  function draw() {
    if (!ctx) return;
    time += 0.015;

    const w = canvas.width;
    const h = canvas.height;
    const rw = w / 2;
    const rh = h / 2;

    ctx.setTransform(2, 0, 0, 2, 0, 0);

    // Generate new spectrum row
    const row = generateSpectrumRow(rw, txStatus.is_running);
    history.push(row);
    const maxRows = Math.floor(rh);
    if (history.length > maxRows) history = history.slice(-maxRows);

    // Draw waterfall (bottom = newest)
    ctx.fillStyle = 'rgba(8, 8, 15, 1)';
    ctx.fillRect(0, 0, rw, rh);

    const rowHeight = rh / history.length;
    for (let y = 0; y < history.length; y++) {
      const dataRow = history[y];
      const yPos = rh - (history.length - y) * rowHeight;
      for (let x = 0; x < rw; x++) {
        const [r, g, b] = valueToColor(dataRow[x]);
        ctx.fillStyle = `rgb(${r},${g},${b})`;
        ctx.fillRect(x, yPos, 1, rowHeight + 0.5);
      }
    }

    // Overlay: frequency scale
    ctx.fillStyle = 'rgba(0, 245, 255, 0.4)';
    ctx.font = '8px "SF Mono", monospace';
    if (txStatus.is_running && txStatus.freq) {
      const freqMHz = (txStatus.freq / 1e6).toFixed(1);
      ctx.fillText(`${freqMHz} MHz`, rw / 2 - 25, 10);
    }

    // Center marker
    ctx.strokeStyle = 'rgba(0, 245, 255, 0.15)';
    ctx.lineWidth = 0.5;
    ctx.setLineDash([3, 3]);
    ctx.beginPath(); ctx.moveTo(rw / 2, 0); ctx.lineTo(rw / 2, rh); ctx.stroke();
    ctx.setLineDash([]);

    animFrame = requestAnimationFrame(draw);
  }
</script>

<div class="panel waterfall-panel">
  <div class="panel-header">
    <span class="panel-icon">📊</span>
    <span class="panel-title">SPECTRUM WATERFALL</span>
    {#if txStatus.is_running}
      <span class="tx-freq">{(txStatus.freq / 1e6).toFixed(3)} MHz</span>
    {/if}
  </div>
  <canvas bind:this={canvas} class="waterfall-canvas"></canvas>
</div>

<style>
  .panel {
    background: rgba(12, 12, 20, 0.7);
    backdrop-filter: blur(24px) saturate(150%);
    -webkit-backdrop-filter: blur(24px) saturate(150%);
    border: 1px solid rgba(0, 245, 255, 0.1);
    border-radius: 16px;
    padding: 16px;
    flex: 1;
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

  .tx-freq {
    margin-left: auto;
    font-size: 10px;
    color: #00f5ff;
    letter-spacing: 0.1em;
  }

  .waterfall-canvas {
    width: 100%;
    height: 280px;
    border-radius: 8px;
    display: block;
  }
</style>
