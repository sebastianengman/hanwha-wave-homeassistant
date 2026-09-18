DOMAIN = "hanwha_wave"
CONF_HOST = "host"
CONF_PORT = "port"
CONF_SSL = "ssl"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
DEFAULT_PORT = 7001
DEFAULT_SCAN_INTERVAL = 30

# WAVE keeps its API documentation in the server itself at /#/api-tool.
# These are the stable legacy REST resources used by current WAVE releases.
CAMERAS_PATH = "/api/cameras"
SNAPSHOT_PATH = "/api/camera/{camera_id}/snapshot"
