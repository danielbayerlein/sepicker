import logging
from freezegun import freeze_time
import pytest
from datetime import datetime
import json

from sepicker.datasinks.mqtt import Mqtt


class TestMqtt:
    @pytest.fixture(autouse=True)
    def mqtt_client_mock(self, mocker):
        return mocker.patch('paho.mqtt.client.Client', autospec=True)

    @pytest.fixture
    def mqtt_instance(self):
        user = 'user'
        password = 'password'  # noqa: S105
        host = 'localhost'
        port = 1883
        topic = 'test/topic'

        return Mqtt(host, port, topic, user, password)

    def test_mqtt_init(self, mqtt_instance):
        assert mqtt_instance.host == 'localhost'
        assert mqtt_instance.port == 1883
        assert mqtt_instance.topic == 'test/topic'
        assert mqtt_instance.user == 'user'
        assert mqtt_instance.password == 'password'  # noqa: S105

    def test_mqtt_enter(self, mqtt_instance, mqtt_client_mock):
        client_instance = mqtt_client_mock.return_value

        with mqtt_instance as mqtt:
            assert mqtt.client == client_instance

        mqtt_client_mock.assert_called_once()
        client_instance.username_pw_set.assert_called_once_with(
            'user',
            'password'
        )
        client_instance.connect.assert_called_once_with('localhost', 1883)
        client_instance.loop_start.assert_called_once()

    def test_mqtt_exit(self, mqtt_instance, mqtt_client_mock):
        with mqtt_instance:
            pass

        client_instance = mqtt_client_mock.return_value
        client_instance.loop_stop.assert_called_once()
        client_instance.disconnect.assert_called_once()

    def test_on_connect(self, mqtt_instance, mocker, caplog):
        client_mock = mocker.Mock()
        with caplog.at_level(logging.DEBUG):
            mqtt_instance.on_connect(client_mock, None, None, 0)
        assert 'CONNACK received with code 0.' in caplog.text

    def test_on_publish(self, mqtt_instance, mocker, caplog):
        client_mock = mocker.Mock()
        with caplog.at_level(logging.DEBUG):
            mqtt_instance.on_publish(client_mock, None, 1)
        assert 'mid: 1' in caplog.text

    @freeze_time("2024-11-10")
    def test_publish(self, mqtt_instance, mqtt_client_mock):
        client_instance = mqtt_client_mock.return_value
        values = [(datetime.now(), 'OUTSIDE_TEMPERATURE', '38.4')]

        with mqtt_instance as mqtt:
            mqtt.publish(values)
            client_instance.publish.assert_called_once_with(
                'test/topic',
                json.dumps([
                    {
                        "timestamp": "2024-11-10T00:00:00",
                        "name": 'OUTSIDE_TEMPERATURE',
                        "value": '38.4'
                    }
                ]),
                retain=True
            )
