from datetime import datetime
import logging
from typing import Optional
import paho.mqtt.client as paho
import json

logger = logging.getLogger(__name__)


class Mqtt:
    def __init__(
            self,
            host: str,
            port: int,
            topic: str,
            user: Optional[str],
            password: Optional[str]
    ) -> None:
        self.host: str = host
        self.port: int = port
        self.topic: str = topic
        self.user: Optional[str] = user
        self.password: Optional[str] = password

    def __enter__(self) -> 'Mqtt':
        client = paho.Client()
        client.on_connect = self.on_connect
        client.on_publish = self.on_publish

        client.username_pw_set(self.user, self.password)
        client.connect(self.host, self.port)
        client.loop_start()

        self.client: paho.Client = client

        return self

    def __exit__(
        self,
        exc_type: type,
        exc_val: Exception,
        exc_tb: type
    ) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(
        self,
        client: paho.Client,
        userdata: Optional[dict],
        flags: int,
        rc: int
    ) -> None:
        logger.debug('CONNACK received with code %d.' % (rc))

    def on_publish(
        self,
        client: paho.Client,
        userdata: Optional[dict],
        mid: int
    ):
        logger.debug("mid: " + str(mid))

    def publish(self, values: list[tuple[datetime, str, int | str]]) -> None:
        payload = [
            {
                "timestamp": timestamp.isoformat(),
                "name": name,
                "value": value
            }
            for inner_list in values
            for timestamp, name, value in [inner_list]
        ]

        self.client.publish(self.topic, json.dumps(payload), retain=True)
