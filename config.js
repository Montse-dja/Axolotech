// config.js — edit this file only when your environment changes

const CONFIG = {
  broker: {
    host:     "ws://10.48.207.30",   // change to wss:// for production
    port:     9001,
    topic:    "axolotech/lake/sensor",
    clientId: "dashboard-" + Math.random().toString(16).slice(2),
  },
  chart: {
    maxPoints: 50,            // rolling window size (number of readings kept)
  },
  thresholds: {
    ph:   { min: 6.5, max: 8.5 }, // alert outside this range
    temp: { min: 14,  max: 20  }, // °C optimal range for axolotls
  },
};
