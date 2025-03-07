import logging
import pytest
import yaml
import os

from sepicker.config import read_config_file, get_mqtt_config, get_mysql_config


def test_read_config_file_success(mocker):
    mock_config_data = {
        'can': {'key1': 'value1'},
        'data': {'key2': 'value2'}
    }
    mock_open = mocker.mock_open(read_data=yaml.dump(mock_config_data))
    mocker.patch('builtins.open', mock_open)
    mocker.patch('os.path.realpath', return_value='/path/to/config.yml')
    mocker.patch('os.path.join', return_value='/path/to/config.yml')

    config = read_config_file()
    assert config == mock_config_data


def test_read_config_file_not_found(mocker, caplog):
    mocker.patch('builtins.open', side_effect=FileNotFoundError)
    mocker.patch('os.path.realpath', return_value='/path/to/config.yml')
    mocker.patch('os.path.join', return_value='/path/to/config.yml')

    with pytest.raises(SystemExit):
        read_config_file()

    with caplog.at_level(logging.INFO):
        assert 'Configuration file "/path/to/config.yml" not found:' \
            in caplog.text


def test_read_config_file_yaml_error(mocker, caplog):
    mock_open = mocker.mock_open()
    mocker.patch('builtins.open', mock_open)
    mocker.patch('os.path.realpath', return_value='/path/to/config.yml')
    mocker.patch('os.path.join', return_value='/path/to/config.yml')
    mocker.patch('yaml.full_load', side_effect=yaml.YAMLError('Invalid YAML'))

    with pytest.raises(SystemExit):
        read_config_file()

    with caplog.at_level(logging.INFO):
        assert 'Configuration file "/path/to/config.yml" not valid:' \
            in caplog.text


def test_mysql_config(mocker):
    mocker.patch.dict(os.environ, {
        'MYSQL_USER': 'test_user',
        'MYSQL_PASSWORD': 'test_password',
        'MYSQL_HOST': 'test_host',
        'MYSQL_DATABASE': 'test_database'
    })

    mysql_config = get_mysql_config()
    assert mysql_config == {
        'user': 'test_user',
        'password': 'test_password',
        'host': 'test_host',
        'database': 'test_database'
    }


def test_mqtt_config(mocker):
    mocker.patch.dict(os.environ, {
        'MQTT_HOST': 'test_mqtt_host',
        'MQTT_PORT': '1883',
        'MQTT_TOPIC': 'test_topic',
        'MQTT_USER': 'test_mqtt_user',
        'MQTT_PASSWORD': 'test_mqtt_password'
    })

    mqtt_config = get_mqtt_config()
    assert mqtt_config == {
        'host': 'test_mqtt_host',
        'port': 1883,
        'topic': 'test_topic',
        'user': 'test_mqtt_user',
        'password': 'test_mqtt_password'
    }
