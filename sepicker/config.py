import yaml
import logging
import sys
import os
import dotenv

dotenv.load_dotenv()

LOGGER = logging.getLogger(__name__)
CONFIG_FILE = 'config.yml'


def _exists(key, value):
    if value is None:
        LOGGER.error('Configuration value for "{key}" not found.')
        sys.exit(1)

    return value


def _read_config_file():
    config = os.path.realpath(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '..',
            CONFIG_FILE
        )
    )
    try:
        with open(config, 'r') as file:
            return yaml.full_load(file)
    except KeyError:
        LOGGER.error('Configuration file "%s" not valid.', config)
        sys.exit(1)
    except FileNotFoundError:
        LOGGER.error('Configuration file "%s" not found.', config)
        sys.exit(1)


yaml_config = _read_config_file()
CAN = yaml_config['can']
DATA = yaml_config['data']
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
DATABASE = {
    'user': _exists('DB_USER', os.getenv('DB_USER')),
    'password': _exists('DB_PASSWORD', os.getenv('DB_PASSWORD')),
    'host': _exists('DB_HOST', os.getenv('DB_HOST')),
    'database': _exists('DB_DATABASE', os.getenv('DB_DATABASE'))
}
