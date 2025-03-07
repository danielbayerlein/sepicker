import logging
import sys
import can

logger = logging.getLogger(__name__)


class CanBus:
    def __init__(self, interface: str, sender: int) -> None:
        self.interface = interface
        self.sender = int(str(sender), 16)
        self.notifier = None
        self.bus = None

    def __enter__(self) -> 'CanBus':
        try:
            self.bus = can.interface.Bus(
                channel=self.interface,
                interface='socketcan'
            )
            return self
        except OSError as e:
            logger.error(
                'Cannot connect to interface "%s": %s',
                self.interface,
                str(e)
            )
            sys.exit(1)

    def __exit__(
            self,
            exc_type: type,
            exc_val: Exception,
            exc_tb: type
    ) -> None:
        if self.notifier:
            self.notifier.stop()

        if self.bus:
            self.bus.shutdown()

    def send(self, data: bytes) -> None:
        msg = can.Message(
            arbitration_id=self.sender,
            is_extended_id=False,
            data=data
        )
        self.bus.send(msg)

    def set_notifier(self, listener: 'can.Listener') -> None:
        self.notifier = can.Notifier(self.bus, [listener])
