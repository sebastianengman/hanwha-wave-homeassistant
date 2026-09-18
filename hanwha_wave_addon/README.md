# Hanwha WAVE Bridge

This Home Assistant app connects to a local Hanwha Wisenet WAVE server and publishes camera snapshots using MQTT discovery. After the app starts, camera entities appear automatically in Home Assistant when the MQTT integration is configured.

Configure the WAVE host, port, HTTPS setting, and a WAVE user with camera-view permission. The MQTT broker defaults to the Home Assistant Mosquitto app.

The WAVE API documentation is available from the WAVE server at `http://<server>:7001/#/api-tool`.
