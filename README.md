# Hanwha WAVE for Home Assistant

Home Assistant app repository for local Hanwha Wisenet WAVE servers.

The main app is **Hanwha WAVE Media Server**. It runs the official WAVE Media Server directly as a Home Assistant app.

## Install the app

1. Open **Settings → Apps → App store** in Home Assistant.
2. Open the three-dot menu and choose **Repositories**.
3. Add `https://github.com/sebastianengman/hanwha-wave-homeassistant`.
4. Install **Hanwha WAVE Bridge**, configure the WAVE and MQTT settings, and start it.

## Install

After starting the app, open its Web UI on port `7001` and complete the WAVE setup wizard. The app stores its WAVE database and configuration persistently.

WAVE exposes its authoritative API documentation in the server itself at `http://<server>:7001/#/api-tool`; API details vary slightly by WAVE release. This integration targets the standard camera and snapshot resources and intentionally keeps credentials in Home Assistant's encrypted config-entry storage.

## Development

```sh
python3 -m compileall custom_components
```

The supplied `login-creds` file is local-only and is ignored by Git.

## Status

Initial release: camera discovery, availability, and snapshots. PTZ, events, recordings, and two-way audio are not yet implemented.
