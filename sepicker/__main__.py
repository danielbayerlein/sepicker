import time
import logging

from .elster.elster import Elster
from .interface.can_bus import CanBus
from .datastore.mysql import save as datastore
from .config import CONFIG

logging.basicConfig(level=logging.INFO)


def main():
    elster = Elster(CONFIG)

    with CanBus(**CONFIG['can']) as can_bus:
        can_bus.notifier(elster.listener)

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
    datastore(elster.values)


if __name__ == '__main__':
    main()
