/**
 * VoidCastFM - Settings Manager
 * Manages user configuration for Pi connection
 * Stored in localStorage for persistence
 */

const DEFAULTS = {
  piHost: '',
  piPort: 8080,
  sshUser: 'pi',
  sshPassword: '', // Not stored - user must enter each session
  autoReconnect: true,
  reconnectInterval: 5000,
};

export class SettingsManager {
  constructor() {
    this.settings = this.load();
  }

  load() {
    try {
      const stored = localStorage.getItem('voidcastfm_settings');
      if (stored) {
        return { ...DEFAULTS, ...JSON.parse(stored) };
      }
    } catch (e) {
      console.warn('Failed to load settings:', e);
    }
    return { ...DEFAULTS };
  }

  save() {
    try {
      localStorage.setItem('voidcastfm_settings', JSON.stringify(this.settings));
    } catch (e) {
      console.warn('Failed to save settings:', e);
    }
  }

  get(key) {
    return this.settings[key] ?? DEFAULTS[key];
  }

  set(key, value) {
    this.settings[key] = value;
    this.save();
  }

  getAll() {
    return { ...this.settings };
  }

  setAll(newSettings) {
    this.settings = { ...DEFAULTS, ...newSettings };
    this.save();
  }

  reset() {
    this.settings = { ...DEFAULTS };
    this.save();
  }

  // Connection string for display
  getConnectionString() {
    const host = this.get('piHost') || 'not configured';
    const port = this.get('piPort');
    return `${host}:${port}`;
  }

  // Check if configured
  isConfigured() {
    return !!this.get('piHost');
  }
}

export const settings = new SettingsManager();
