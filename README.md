# Hanwha WAVE for Home Assistant

Home Assistant app repository for local Hanwha Wisenet WAVE servers.

The main app is **Hanwha WAVE Bridge**. It runs as a Home Assistant app and publishes WAVE cameras and JPEG snapshots through MQTT discovery.

## Install the app

1. Open **Settings → Apps → App store** in Home Assistant.
2. Open the three-dot menu and choose **Repositories**.
3. Add `https://github.com/sebastianengman/hanwha-wave-homeassistant`.
4. Install **Hanwha WAVE Bridge**, configure the WAVE and MQTT settings, and start it.

## Install

The app needs a WAVE server address, API port (normally `7001`), and a WAVE user with permission to view cameras. MQTT discovery must be enabled in Home Assistant; the official Mosquitto app is the simplest broker.

WAVE exposes its authoritative API documentation in the server itself at `http://<server>:7001/#/api-tool`; API details vary slightly by WAVE release. This integration targets the standard camera and snapshot resources and intentionally keeps credentials in Home Assistant's encrypted config-entry storage.

## Development

```sh
python3 -m compileall custom_components
```

The supplied `login-creds` file is local-only and is ignored by Git.

## Status

Initial release: camera discovery, availability, and snapshots. PTZ, events, recordings, and two-way audio are not yet implemented.
