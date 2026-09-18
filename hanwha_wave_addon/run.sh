#!/usr/bin/env bash

set -euo pipefail

BASE_DIR=/opt/hanwha/mediaserver
PERSISTENT_DIR=/config/wave

mkdir -p "${PERSISTENT_DIR}/var" "${PERSISTENT_DIR}/etc"

# WAVE stores its database, recordings metadata and configuration below /opt.
# Move those mutable directories to the app's persistent config volume once.
if [[ ! -e "${PERSISTENT_DIR}/.initialized" ]]; then
  if [[ -d "${BASE_DIR}/var" ]]; then
    cp -a "${BASE_DIR}/var/." "${PERSISTENT_DIR}/var/"
  fi
  if [[ -d "${BASE_DIR}/etc" ]]; then
    cp -a "${BASE_DIR}/etc/." "${PERSISTENT_DIR}/etc/"
  fi
  touch "${PERSISTENT_DIR}/.initialized"
fi

rm -rf "${BASE_DIR}/var" "${BASE_DIR}/etc"
ln -s "${PERSISTENT_DIR}/var" "${BASE_DIR}/var"
ln -s "${PERSISTENT_DIR}/etc" "${BASE_DIR}/etc"
chown -R hanwha:hanwha "${PERSISTENT_DIR}"

echo "Starting Hanwha WAVE Media Server on port 7001"
exec su -s /bin/bash hanwha -c "${BASE_DIR}/lib/scripts/systemd_mediaserver_start.sh"
