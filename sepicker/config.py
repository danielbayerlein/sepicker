import yaml
import logging
import sys
import os
import dotenv

LOGGER = logging.getLogger(__name__)

dotenv.load_dotenv()


def _load():
    config = os.path.abspath(os.getenv('CONFIG_FILE'))

    try:
        with open(config, 'r') as file:
            return yaml.full_load(file)
    except KeyError:
        LOGGER.error('Configuration file "%s" not valid.', config)
        sys.exit(1)
    except FileNotFoundError:
        LOGGER.error('Configuration file "%s" not found.', config)
        sys.exit(1)


CONFIG = _load()

DB_USER = os.environ('DB_USER')
DB_PASSWORD = os.environ('DB_PASSWORD')
DB_HOST = os.environ('DB_HOST')
DB_DATABASE = os.environ('DB_DATABASE')
