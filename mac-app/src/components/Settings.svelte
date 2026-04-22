<script>
  import { api, settings } from '../lib/api.js';

  let { onClose } = $props();

  // Local state for form
  let piHost = $state(settings.get('piHost'));
  let piPort = $state(settings.get('piPort'));
  let sshUser = $state(settings.get('sshUser'));
  let autoReconnect = $state(settings.get('autoReconnect'));
  let showPassword = $state(false);
  let testStatus = $state(null);
  let testing = $state(false);

  function saveSettings() {
    settings.set('piHost', piHost);
    settings.set('piPort', parseInt(piPort) || 8080);
    settings.set('sshUser', sshUser);
    settings.set('autoReconnect', autoReconnect);
    
    // Update API connection
    api.updateFromSettings();
    
    onClose?.();
  }

  function resetSettings() {
    settings.reset();
    piHost = settings.get('piHost');
    piPort = settings.get('piPort');
    sshUser = settings.get('sshUser');
    autoReconnect = settings.get('autoReconnect');
    api.updateFromSettings();
  }

  async function testConnection() {
    testing = true;
    testStatus = null;
    
    try {
      const response = await fetch(`${api.baseUrl}/`, {
        method: 'GET',
        signal: AbortSignal.timeout(5000)
      });
      
      if (response.ok) {
        const data = await response.json();
        testStatus = {
          success: true,
          message: `Connected to ${data.name || 'Pi'} v${data.version || '?'}`,
          details: data
        };
      } else {
        testStatus = {
          success: false,
          message: `HTTP ${response.status}: ${response.statusText}`
        };
      }
    } catch (error) {
      testStatus = {
        success: false,
        message: error.name === 'AbortError' 
          ? 'Connection timeout (5s)' 
          : `Error: ${error.message}`
      };
    } finally {
      testing = false;
    }
  }
</script>

<div class="modal-overlay" onclick={onClose}>
  <div class="modal-content" onclick={e => e.stopPropagation()}>
    <div class="modal-header">
      <h2>⚙️ Connection Settings</h2>
      <button class="close-btn" onclick={onClose}>×</button>
    </div>

    <div class="modal-body">
      <div class="settings-section">
        <h3>Raspberry Pi Connection</h3>
        <p class="help-text">
          Enter the IP address or hostname of your Raspberry Pi running the VoidCastFM backend.
        </p>

        <div class="form-group">
          <label for="pi-host">Pi Hostname/IP</label>
          <input
            id="pi-host"
            type="text"
            class="form-input"
            bind:value={piHost}
            placeholder="e.g., 192.168.1.25 or pi0.local"
          />
          <span class="form-help">Current: {settings.get('piHost') || 'not set'}</span>
        </div>

        <div class="form-group">
          <label for="pi-port">Pi Port</label>
          <input
            id="pi-port"
            type="number"
            class="form-input"
            bind:value={piPort}
            min="1"
            max="65535"
          />
          <span class="form-help">Default: 8080</span>
        </div>

        <div class="form-group">
          <label for="ssh-user">SSH Username</label>
          <input
            id="ssh-user"
            type="text"
            class="form-input"
            bind:value={sshUser}
            placeholder="e.g., pi"
          />
          <span class="form-help">For remote management (optional)</span>
        </div>

        <div class="form-group checkbox-group">
          <input
            id="auto-reconnect"
            type="checkbox"
            bind:checked={autoReconnect}
          />
          <label for="auto-reconnect">Auto-reconnect on disconnect</label>
        </div>
      </div>

      <div class="settings-section">
        <h3>Test Connection</h3>
        <p class="help-text">
          Verify that VoidCastFM can reach your Raspberry Pi.
        </p>

        <button
          class="test-btn"
          onclick={testConnection}
          disabled={testing || !piHost}
        >
          {testing ? 'Testing...' : '🔍 Test Connection'}
        </button>

        {#if testStatus}
          <div class="test-result" class:success={testStatus.success}>
            <span class="result-icon">{testStatus.success ? '✅' : '❌'}</span>
            <span class="result-message">{testStatus.message}</span>
          </div>
        {/if}
      </div>
    </div>

    <div class="modal-footer">
      <button class="btn-secondary" onclick={resetSettings}>
        Reset to Defaults
      </button>
      <button class="btn-primary" onclick={saveSettings}>
        Save Settings
      </button>
    </div>
  </div>
</div>

<style>
  .modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    animation: fadeIn 0.2s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .modal-content {
    background: rgba(12, 12, 20, 0.95);
    border: 1px solid rgba(0, 245, 255, 0.2);
    border-radius: 16px;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid rgba(0, 245, 255, 0.1);
  }

  .modal-header h2 {
    font-size: 18px;
    margin: 0;
    background: linear-gradient(135deg, #00f5ff, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .close-btn {
    background: none;
    border: none;
    color: rgba(224, 230, 240, 0.5);
    font-size: 24px;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 4px;
  }

  .close-btn:hover {
    background: rgba(0, 245, 255, 0.1);
    color: #00f5ff;
  }

  .modal-body {
    padding: 20px;
  }

  .settings-section {
    margin-bottom: 24px;
  }

  .settings-section h3 {
    font-size: 14px;
    color: #00f5ff;
    margin-bottom: 8px;
    letter-spacing: 0.1em;
  }

  .help-text {
    font-size: 11px;
    color: rgba(224, 230, 240, 0.5);
    margin-bottom: 16px;
    line-height: 1.5;
  }

  .form-group {
    margin-bottom: 16px;
  }

  .form-group label {
    display: block;
    font-size: 11px;
    letter-spacing: 0.1em;
    color: rgba(0, 245, 255, 0.7);
    margin-bottom: 6px;
    text-transform: uppercase;
  }

  .form-input {
    width: 100%;
    padding: 10px 12px;
    background: rgba(0, 245, 255, 0.05);
    border: 1px solid rgba(0, 245, 255, 0.15);
    border-radius: 8px;
    color: #e0e6f0;
    font-family: 'SF Mono', monospace;
    font-size: 14px;
    outline: none;
    transition: all 0.2s ease;
  }

  .form-input:focus {
    border-color: rgba(0, 245, 255, 0.4);
    box-shadow: 0 0 16px rgba(0, 245, 255, 0.1);
  }

  .form-help {
    display: block;
    font-size: 10px;
    color: rgba(224, 230, 240, 0.4);
    margin-top: 4px;
  }

  .checkbox-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .checkbox-group input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: #00f5ff;
  }

  .checkbox-group label {
    margin: 0 !important;
    text-transform: none !important;
    letter-spacing: normal !important;
    font-size: 12px !important;
  }

  .test-btn {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid rgba(139, 92, 246, 0.3);
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.12), rgba(0, 200, 255, 0.06));
    color: #c4b5fd;
    font-family: inherit;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    cursor: pointer;
    transition: all 0.25s ease;
  }

  .test-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.22), rgba(0, 200, 255, 0.12));
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.15);
  }

  .test-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .test-result {
    margin-top: 12px;
    padding: 12px;
    border-radius: 8px;
    background: rgba(255, 60, 60, 0.1);
    border: 1px solid rgba(255, 60, 60, 0.2);
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
  }

  .test-result.success {
    background: rgba(0, 245, 255, 0.1);
    border-color: rgba(0, 245, 255, 0.3);
  }

  .result-icon {
    font-size: 16px;
  }

  .modal-footer {
    display: flex;
    gap: 12px;
    padding: 20px;
    border-top: 1px solid rgba(0, 245, 255, 0.1);
  }

  .btn-secondary {
    flex: 1;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid rgba(224, 230, 240, 0.2);
    background: rgba(224, 230, 240, 0.05);
    color: rgba(224, 230, 240, 0.7);
    font-family: inherit;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    cursor: pointer;
    transition: all 0.25s ease;
  }

  .btn-secondary:hover {
    background: rgba(224, 230, 240, 0.1);
    color: #e0e6f0;
  }

  .btn-primary {
    flex: 2;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid rgba(0, 245, 255, 0.3);
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.15), rgba(0, 200, 255, 0.08));
    color: #00f5ff;
    font-family: inherit;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    cursor: pointer;
    transition: all 0.25s ease;
  }

  .btn-primary:hover {
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.25), rgba(0, 200, 255, 0.15));
    box-shadow: 0 0 24px rgba(0, 245, 255, 0.2);
  }
</style>
