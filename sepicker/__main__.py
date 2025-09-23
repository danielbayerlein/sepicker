import time
import logging

from .elster.elster import Elster
from .interface.can_bus import CanBus
from .datasinks.mysql import Mysql
from .datasinks.mqtt import Mqtt
from .config import (
    LOG_LEVEL,
    read_config_file,
    get_mqtt_config,
    get_mysql_config
)

logging.basicConfig(level=LOG_LEVEL)


def main():
    config = read_config_file()
    elster = Elster(sender=config['can']['sender'], items=config['data'])

    with CanBus(**config['can']) as can_bus:
        can_bus.set_notifier(elster.listener)

        for frame in elster.frames:
            can_bus.send(frame.message())
            time.sleep(0.01)

        # Wait for response
        timeout = 0
        while elster.is_done() is False:
            timeout += 1
            time.sleep(0.5)

            if timeout == 10:
                logging.error('TimeoutError: Not all data received.')
                break

    # Save result
    mysql_config = get_mysql_config()
    if mysql_config['host']:
        with Mysql(**mysql_config) as db:
            db.save(elster.values)

    mqtt_config = get_mqtt_config()
    if mqtt_config['host']:
        with Mqtt(**mqtt_config) as mqtt:
            mqtt.publish(elster.values)


if __name__ == '__main__':
    main()
