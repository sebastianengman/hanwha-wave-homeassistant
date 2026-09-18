# Hanwha WAVE for Home Assistant

Custom Home Assistant integration for local Hanwha Wisenet WAVE servers.

## Install

Copy `custom_components/hanwha_wave` into `/config/custom_components/hanwha_wave`, restart Home Assistant, then add **Hanwha WAVE** from Settings → Devices & services.

Enter the WAVE server address, API port (normally `7001`), and a WAVE user with permission to view cameras. The integration discovers cameras and provides snapshot camera entities.

WAVE exposes its authoritative API documentation in the server itself at `http://<server>:7001/#/api-tool`; API details vary slightly by WAVE release. This integration targets the standard camera and snapshot resources and intentionally keeps credentials in Home Assistant's encrypted config-entry storage.

## Development

```sh
python3 -m compileall custom_components
```

The supplied `login-creds` file is local-only and is ignored by Git.

## Status

Initial release: camera discovery, availability, state metadata, and snapshots. PTZ, events, recordings, and two-way audio are not yet implemented.
