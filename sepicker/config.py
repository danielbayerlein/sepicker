import yaml
import logging
import sys
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
CONFIG_FILE: str = 'config.yml'


def read_config_file() -> dict:
    config: str = os.path.realpath(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '..',
            CONFIG_FILE
        )
    )
    try:
        with open(config, 'r') as file:
            return yaml.full_load(file)
    except yaml.YAMLError as e:
        logger.error(f'Configuration file "{config}" not valid: {e}')
        sys.exit(1)
    except FileNotFoundError as e:
        logger.error(f'Configuration file "{config}" not found: {e}')
        sys.exit(1)


def get_mysql_config() -> dict:
    return {
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'host': os.getenv('MYSQL_HOST'),
        'database': os.getenv('MYSQL_DATABASE')
    }


def get_mqtt_config() -> dict:
    return {
        'host': os.getenv('MQTT_HOST'),
        'port': int(os.getenv('MQTT_PORT', '1883')),
        'topic': os.getenv('MQTT_TOPIC'),
        'user': os.getenv('MQTT_USER'),
        'password': os.getenv('MQTT_PASSWORD'),
    }


LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
