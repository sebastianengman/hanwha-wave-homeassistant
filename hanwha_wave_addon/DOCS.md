# Hanwha WAVE Media Server

Open the Web UI on port 7001 after starting the app. The first-run WAVE setup wizard creates the administrator account and system. The app does not store WAVE credentials in the repository.

The official WAVE package stores its mutable database and configuration under the app's persistent `/config/wave` directory. Camera recordings should be configured on a dedicated disk or network share from the WAVE Web Admin interface.

This app currently supports the amd64 architecture because the official installer supplied by Hanwha is `linux_x64`.
