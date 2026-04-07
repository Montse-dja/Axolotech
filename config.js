// config.js — edit this file only when your environment changes

const CONFIG = {
  broker: {
    host:     "ws://192.168.1.100",  // change to wss:// for prod
    port:     9001,
    topic:    "axolotech/lake/sensor",
    clientId: "dashboard-" + Math.random().toString(16).slice(2),
  },
  chart: {
    maxPoints: 100,           // rolling window size
  },
  thresholds: {
    ph:   { min: 6.5, max: 8.5 }, // alert outside this range
    temp: { min: 14,  max: 20  }, // °C comfort range for axolotls
  },
};
