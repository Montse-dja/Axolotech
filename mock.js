// mock.js — development simulator
// Replaces the real MQTT connection with a fake one that generates sensor data.
// REMOVE the <script src="mock.js"> line from index.html before connecting real hardware.

(function () {

  // How often a fake reading is emitted (milliseconds)
  const INTERVAL_MS = 2000;

  // Starting values — drift from here
  let ph     = 7.2;
  let temp   = 17.0;
  let readingCount = 0;

  // Small random walk — keeps values realistic and occasionally triggers alerts
  function drift(value, step, min, max) {
    const delta = (Math.random() - 0.5) * step;
    return Math.min(max, Math.max(min, value + delta));
  }

  // Fake axolotl detections: present roughly 30% of the time
  function fakePresence() {
    return Math.random() < 0.30;
  }

  // Build a fake payload matching the real device format
  function makePayload() {
    ph   = drift(ph,   0.15, 5.5, 9.5);
    temp = drift(temp, 0.4,  10,  28);

    const present    = fakePresence();
    const confidence = present ? 0.70 + Math.random() * 0.29 : Math.random() * 0.25;

    return JSON.stringify({
      timestamp:       new Date().toISOString(),
      ph:              parseFloat(ph.toFixed(2)),
      temp_c:          parseFloat(temp.toFixed(1)),
      axolotl_present: present,
      confidence:      parseFloat(confidence.toFixed(2)),
    });
  }

  // ── Fake MQTT client ─────────────────────────────────────
  // mqtt.connect() normally returns a client object.
  // We replace window.mqtt with a mock that looks identical to the real library
  // so app.js never knows the difference.

  const fakeClient = {
    _handlers: {},

    on(event, fn) {
      this._handlers[event] = fn;
      return this;
    },

    subscribe(_topic, _opts, cb) {
      if (cb) cb(null);
      return this;
    },

    end() {},

    _emit(event, ...args) {
      if (this._handlers[event]) this._handlers[event](...args);
    },
  };

  window.mqtt = {
    connect(_url, _opts) {
      // Fire "connect" on next tick so app.js has time to register handlers
      setTimeout(() => {
        fakeClient._emit("connect");

        // Start emitting fake messages
        setInterval(() => {
          readingCount++;
          const payload = makePayload();
          fakeClient._emit("message", CONFIG.broker.topic, payload);
        }, INTERVAL_MS);
      }, 600);

      return fakeClient;
    },
  };

  // Banner so you never forget mock mode is on
  const banner = document.createElement("div");
  banner.style.cssText = `
    position: fixed;
    bottom: 16px;
    right: 16px;
    background: #5c3f10;
    color: #e8a838;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    padding: 6px 14px;
    border-radius: 4px;
    border: 1px solid #e8a838;
    z-index: 9999;
    letter-spacing: 0.06em;
  `;
  banner.textContent = "SIMULATION MODE — not connected to real hardware";
  document.body.appendChild(banner);

  console.info("[mock.js] Simulation active — remove mock.js script tag for real hardware");

})();git add mock.js config.js index.html
git commit -m "add simulation mode + update IP and maxPoints"
git push
