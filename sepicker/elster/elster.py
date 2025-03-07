import ctypes
import logging
from datetime import datetime
import can
from .elster_frame import ElsterFrame

logger = logging.getLogger(__name__)


class Elster:
    RESPONSE: int = 0x2

    def __init__(self, sender: int, items: list) -> None:
        self.frames: list[ElsterFrame] = [
            ElsterFrame(**item) for item in items
        ]
        self.values: list[tuple] = []
        self.datetime = datetime.now()
        self.sender: int = int(str(sender), 16)

    def listener(self, msg: 'can.Message') -> None:
        data: bytearray = msg.data

        receiver = (data[0] & 0xf0) * 8 + (data[1] & 0x7f)
        msg_type = data[0] & 0x0f

        if msg_type != self.RESPONSE or \
           receiver != self.sender or \
           not self._exist_receiver(msg.arbitration_id):
            return

        if data[2] == 0xfa:
            register: int = ((data[3] & 0xff) << 8) | (data[4] & 0xff)
            if len(data) == 7:
                value: int = ctypes.c_int16(
                    ((data[5] & 0xff) << 8) | (data[6] & 0xff)
                ).value
        else:
            register = data[2]
            if len(data) >= 5:
                value = ctypes.c_int16(
                    ((data[3] & 0xff) << 8) | (data[4] & 0xff)
                ).value

        entry = self._get_frame(msg.arbitration_id, register)

        self.values.append(
            (self.datetime, entry.name, entry.formatter(value))
        )

    def is_done(self) -> bool:
        return len(self.values) == len(self.frames)

    def _exist_receiver(self, receiver: int) -> bool:
        frames = [frame for frame in self.frames if frame.receiver == receiver]
        return len(frames) > 0

    def _get_frame(self, receiver: int, register: int) -> 'ElsterFrame':
        for frame in self.frames:
            if frame.receiver == receiver and frame.register == register:
                return frame
