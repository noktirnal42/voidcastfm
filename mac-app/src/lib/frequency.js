/**
 * PHANTOM CONTROLLER — Frequency Utilities
 */

// Amateur radio band plans (US)
export const BANDS = [
  { name: '2200m',  low: 135700,   high: 137800,   label: '2200m (LF)' },
  { name: '630m',   low: 472000,   high: 479000,   label: '630m (MF)' },
  { name: '160m',   low: 1800000,  high: 2000000,  label: '160m' },
  { name: '80m',    low: 3500000,  high: 4000000,  label: '80m' },
  { name: '60m',    low: 5330500,  high: 5406500,  label: '60m' },
  { name: '40m',    low: 7000000,  high: 7300000,  label: '40m' },
  { name: '30m',    low: 10100000, high: 10150000, label: '30m' },
  { name: '20m',    low: 14000000, high: 14350000, label: '20m' },
  { name: '17m',    low: 18068000, high: 18168000, label: '17m' },
  { name: '15m',    low: 21000000, high: 21450000, label: '15m' },
  { name: '12m',    low: 24890000, high: 24990000, label: '12m' },
  { name: '10m',    low: 28000000, high: 29700000, label: '10m' },
  { name: '6m',     low: 50000000, high: 54000000, label: '6m' },
  { name: '2m',     low: 144000000,high: 148000000,label: '2m' },
  { name: '1.25m',  low: 222000000,high: 225000000,label: '1.25m' },
  { name: '70cm',   low: 420000000,high: 450000000,label: '70cm' },
  { name: 'FM',     low: 87500000, high: 108000000,label: 'FM Broadcast' },
  { name: 'ISM',    low: 433000000,high: 435000000,label: 'ISM 434MHz' },
];

export function formatFreq(hz) {
  if (hz >= 1e9) return (hz / 1e9).toFixed(3) + ' GHz';
  if (hz >= 1e6) return (hz / 1e6).toFixed(3) + ' MHz';
  if (hz >= 1e3) return (hz / 1e3).toFixed(1) + ' kHz';
  return hz + ' Hz';
}

export function parseFreq(str) {
  str = str.trim().toLowerCase();
  let multiplier = 1;
  if (str.endsWith('ghz')) { multiplier = 1e9; str = str.replace('ghz', ''); }
  else if (str.endsWith('mhz')) { multiplier = 1e6; str = str.replace('mhz', ''); }
  else if (str.endsWith('khz')) { multiplier = 1e3; str = str.replace('khz', ''); }
  const num = parseFloat(str);
  if (isNaN(num)) return null;
  return Math.round(num * multiplier);
}

export function getBandForFreq(hz) {
  return BANDS.find(b => hz >= b.low && hz <= b.high) || null;
}

export function antennaLength(hz) {
  // Quarter-wave in meters
  return 75 / (hz / 1e6);
}

export const MODES = [
  { id: 'fm',    label: 'FM',     icon: '📻', description: 'Frequency Modulation' },
  { id: 'am',    label: 'AM',     icon: '📡', description: 'Amplitude Modulation' },
  { id: 'ssb',   label: 'SSB',    icon: '🗣️', description: 'Single Sideband (USB)' },
  { id: 'vfo',   label: 'VFO',    icon: '〰️', description: 'Carrier / CW' },
  { id: 'iq',    label: 'IQ',     icon: '🧠', description: 'SDR I/Q Stream' },
  { id: 'chirp', label: 'CHIRP',  icon: '↗️', description: 'Frequency Sweep' },
];
