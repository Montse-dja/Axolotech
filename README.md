# Welcome to Axolotech
Hi! We are Monterrat, Azul, Alleine and Luis! We are a group of electronic engineers specialized on cyber-physical systems. This is the hub we are using for our proyect, stay tuned for updates and development!

The project consits of an IoT system used for the monitoring of water and detection of Axolotls or other fishes. This information is sent via MQTT to a webpage where a timeseries of the data and the quantity of the detections can be found. This webpage gives alertes, whenever a parameter is out of the suggested range.

The python and arduino code are conjoined using the Arduino Uno Q Bridge to send data from one to the other.


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
