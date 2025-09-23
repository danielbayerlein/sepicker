import logging
from typing import Dict

logger = logging.getLogger(__name__)


class ElsterFrame:
    READ: int = 0x1

    def __init__(self, name: str, index: str, format: str | None = None):
        receiver, register = index.split('.')
        self.name: str = name
        self.receiver: int = int(receiver, 16)
        self.register: int = int(register, 16)
        self.format: str | None = format

    def message(self) -> list[int]:
        msg: list[int] = [0] * 5
        msg[0] = (self.READ & 0xf) | ((self.receiver >> 3) & 0xf0)
        msg[1] = self.receiver & 0x7f
        msg[2] = 0xfa
        msg[3] = self.register >> 8
        msg[4] = self.register & 0xff

        return msg

    def formatter(self, value: int) -> int | str:
        if not self.format:
            return value

        formats: Dict[str, callable] = {
            'dec_val': lambda x: '{:.1f}'.format(x / 10.0),
            'mil_val': lambda x: '{:.3f}'.format(x / 1000.0),
            'little_endian': lambda x: '{:d}'.format(
                (x >> 8) + 256 * (x & 0xff)
            )
        }
        return formats[self.format](value)
