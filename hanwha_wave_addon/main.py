#!/usr/bin/env python3
"""Small WAVE-to-MQTT bridge for the Home Assistant app runtime."""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

import paho.mqtt.client as mqtt
import requests

LOG = logging.getLogger("hanwha_wave")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def options() -> dict[str, Any]:
    with open("/data/options.json", encoding="utf-8") as file:
        return json.load(file)


class Bridge:
    def __init__(self, config: dict[str, Any]) -> None:
        scheme = "https" if config["wave_ssl"] else "http"
        self.base = f"{scheme}://{config['wave_host']}:{config['wave_port']}".rstrip("/")
        self.auth = (config["wave_username"], config["wave_password"])
        self.interval = config["scan_interval"]
        self.mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="hanwha-wave-bridge")
        if config.get("mqtt_username"):
            self.mqtt.username_pw_set(config["mqtt_username"], config.get("mqtt_password", ""))
        self.mqtt_host = config["mqtt_host"]
        self.mqtt_port = config["mqtt_port"]

    def wave_get(self, path: str) -> requests.Response:
        response = requests.get(f"{self.base}{path}", auth=self.auth, timeout=15, verify=False)
        response.raise_for_status()
        return response

    def cameras(self) -> list[dict[str, Any]]:
        payload = self.wave_get("/api/cameras").json()
        items = payload.get("cameras", payload) if isinstance(payload, dict) else payload
        return [item for item in items if isinstance(item, dict)]

    @staticmethod
    def camera_id(camera: dict[str, Any]) -> str:
        return str(camera.get("id") or camera.get("cameraId") or camera.get("guid") or "")

    def publish_discovery(self, camera: dict[str, Any], camera_id: str) -> None:
        name = str(camera.get("name") or camera.get("caption") or camera_id)
        topic = f"hanwha_wave/{camera_id}"
        device = {"identifiers": [f"hanwha_wave_{camera_id}"], "name": name, "manufacturer": "Hanwha", "model": "Wisenet WAVE"}
        config = {
            "name": name,
            "unique_id": f"hanwha_wave_camera_{camera_id}",
            "topic": f"{topic}/snapshot",
            "availability_topic": f"{topic}/availability",
            "device": device,
        }
        self.mqtt.publish(f"homeassistant/camera/hanwha_wave_{camera_id}/config", json.dumps(config), retain=True)

    def poll(self) -> None:
        cameras = self.cameras()
        for camera in cameras:
            camera_id = self.camera_id(camera)
            if not camera_id:
                continue
            topic = f"hanwha_wave/{camera_id}"
            self.publish_discovery(camera, camera_id)
            try:
                snapshot = self.wave_get(f"/api/camera/{camera_id}/snapshot").content
                self.mqtt.publish(f"{topic}/snapshot", snapshot, retain=False)
                self.mqtt.publish(f"{topic}/availability", "online", retain=True)
            except requests.RequestException as error:
                LOG.warning("Could not read snapshot for %s: %s", camera_id, error)
                self.mqtt.publish(f"{topic}/availability", "offline", retain=True)

    def run(self) -> None:
        while True:
            try:
                self.mqtt.connect(self.mqtt_host, self.mqtt_port, keepalive=60)
                self.mqtt.loop_start()
                LOG.info("Connected to MQTT and WAVE at %s", self.base)
                while True:
                    self.poll()
                    time.sleep(self.interval)
            except (OSError, requests.RequestException, ValueError) as error:
                LOG.warning("Bridge temporarily unavailable: %s", error)
                try:
                    self.mqtt.loop_stop()
                    self.mqtt.disconnect()
                except Exception:  # noqa: BLE001
                    pass
                time.sleep(15)


if __name__ == "__main__":
    Bridge(options()).run()
