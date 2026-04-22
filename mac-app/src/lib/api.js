/**
 * VoidCastFM — API Client
 * REST + WebSocket communication with Pi backend
 * Connection settings are configurable via SettingsManager
 */

import { settings } from './settings.js';

// Detect if we're in Vite dev mode (served from localhost:5173)
const isDevProxy = typeof window !== 'undefined' &&
  window.location.hostname === 'localhost' &&
  window.location.port === '5173';

export class VoidCastAPI {
  constructor() {
    this.ws = null;
    this.wsListeners = new Map();
    this.reconnectTimer = null;
    this.connected = false;
    this.onStatusUpdate = null;
    this.onConnectionChange = null;
    
    // Load settings
    this.updateFromSettings();
  }

  updateFromSettings() {
    this.host = settings.get('piHost');
    this.port = settings.get('piPort');
  }

  get baseUrl() {
    // In dev mode, route through Vite proxy at /api
    if (isDevProxy) return '/api';
    const host = this.host || 'localhost';
    const port = this.port || 8080;
    return `http://${host}:${port}`;
  }

  get wsUrl() {
    // In dev mode, use the /ws proxy
    if (isDevProxy) {
      const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      return `${proto}//${window.location.host}/ws`;
    }
    const host = this.host || 'localhost';
    const port = this.port || 8080;
    return `ws://${host}:${port}/ws`;
  }

  // ─── REST API ─────────────────────────────────────

  async fetch(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const res = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
    if (!res.ok) throw new Error(`API Error: ${res.status} ${res.statusText}`);
    return res.json();
  }

  async getStatus() {
    return this.fetch('/status');
  }

  async startTX(freq, mode, { power = 1, ppm = 0, rds_ps = null, rds_rt = null } = {}) {
    return this.fetch('/tx/start', {
      method: 'POST',
      body: JSON.stringify({ freq, mode, power, ppm, rds_ps, rds_rt }),
    });
  }

  async stopTX() {
    return this.fetch('/tx/stop', { method: 'POST' });
  }

  async playFile(file, freq, mode = 'fm') {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${this.baseUrl}/tx/play_file?freq=${freq}&mode=${mode}`, {
      method: 'POST',
      body: formData,
    });
    return res.json();
  }

  async startIQ(freq, port = 8011, sampleRate = 48000) {
    return this.fetch('/tx/iq/start', {
      method: 'POST',
      body: JSON.stringify({ freq, port, sample_rate: sampleRate }),
    });
  }

  async stopIQ() {
    return this.fetch('/tx/iq/stop', { method: 'POST' });
  }

  async startAudioStream(freq, mode = 'fm', port = 5000) {
    return this.fetch('/stream/audio/start', {
      method: 'POST',
      body: JSON.stringify({ freq, mode, port }),
    });
  }

  async stopAudioStream() {
    return this.fetch('/stream/audio/stop', { method: 'POST' });
  }

  async getSystem() {
    return this.fetch('/system');
  }

  // ─── Soundboard API ─────────────────────────────────

  async getTones() {
    return this.fetch('/soundboard/tones');
  }

  async playTone(toneId, freq = 100000000, mode = 'fm') {
    return this.fetch(`/soundboard/play/${toneId}?freq=${freq}&mode=${mode}`, {
      method: 'POST',
    });
  }

  async stopTone() {
    return this.fetch('/soundboard/stop', { method: 'POST' });
  }

  // ─── WebSocket ────────────────────────────────────

  connectWS() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) return;

    try {
      this.ws = new WebSocket(this.wsUrl);

      this.ws.onopen = () => {
        this.connected = true;
        this.onConnectionChange?.(true);
        if (this.reconnectTimer) {
          clearInterval(this.reconnectTimer);
          this.reconnectTimer = null;
        }
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.onStatusUpdate?.(data);

          // Notify named listeners
          const type = data.type;
          if (this.wsListeners.has(type)) {
            this.wsListeners.get(type).forEach(cb => cb(data));
          }
        } catch (e) {
          console.warn('WS parse error:', e);
        }
      };

      this.ws.onclose = () => {
        this.connected = false;
        this.onConnectionChange?.(false);
        this.scheduleReconnect();
      };

      this.ws.onerror = () => {
        this.connected = false;
        this.onConnectionChange?.(false);
      };

    } catch (e) {
      this.scheduleReconnect();
    }
  }

  scheduleReconnect() {
    if (this.reconnectTimer) return;
    this.reconnectTimer = setInterval(() => {
      this.connectWS();
    }, 5000);
  }

  disconnectWS() {
    if (this.reconnectTimer) {
      clearInterval(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.connected = false;
    this.onConnectionChange?.(false);
  }

  sendWS(data) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  on(type, callback) {
    if (!this.wsListeners.has(type)) {
      this.wsListeners.set(type, []);
    }
    this.wsListeners.get(type).push(callback);
  }

  off(type, callback) {
    if (this.wsListeners.has(type)) {
      const list = this.wsListeners.get(type);
      const idx = list.indexOf(callback);
      if (idx > -1) list.splice(idx, 1);
    }
  }
}

export const api = new VoidCastAPI();

// Export settings reference for components to use
export { settings };
