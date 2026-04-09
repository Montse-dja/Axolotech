# Welcome to Axolotech
Hi! We are Montserrat, Azul, Alleine, and Luis. We are a group of electronic engineers specialized in cyber-physical systems. This is the hub we are using for our project—stay tuned for updates and development!

The project consists of an IoT system used for monitoring water conditions and detecting axolotls or other fish. This information is sent via MQTT to a webpage, where a time series of the data and the number of detections can be viewed. The webpage generates alerts whenever a parameter is outside the suggested range.

The Python and Arduino code are integrated using the Arduino Uno Q Bridge to send data between the two systems.

## Current known limitations / next steps

- Historical data lives only in browser memory — lost on page refresh
- No authentication on the MQTT connection
- Single device / single topic
- GitHub Pages + local broker requires WSS or a tunnel (ngrok, Cloudflare Tunnel)

## Bricks Used
- Database - TimeSeries
- WebUI - HTML
- Video Object Detection

## Sketch Libraries

- OneWire 2.3.8
- DallasTemperature 4.0.6
- Arduino_RouterBridge 0.4.1
