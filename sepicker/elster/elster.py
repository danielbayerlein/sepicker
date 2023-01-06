import ctypes
import logging
from datetime import datetime
from .elster_frame import ElsterFrame

LOGGER = logging.getLogger(__name__)


class Elster:
    RESPONSE = 0x2

    def __init__(self, sender, items):
        self.frames = [ElsterFrame(**item) for item in items]
        self.values = []
        self.datetime = datetime.now()
        self.sender = int(str(sender), 16)

    def listener(self, msg):
        data = msg.data

        receiver = (data[0] & 0xf0) * 8 + (data[1] & 0x7f)
        type = data[0] & 0x0f

        if type != self.RESPONSE or \
           receiver != self.sender or \
           not self._exist_receiver(msg.arbitration_id):
            return

        if data[2] == 0xfa:
            register = ((data[3] & 0xff) << 8) | (data[4] & 0xff)
            if len(data) == 7:
                value = ctypes.c_int16(
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

    def is_done(self):
        return len(self.values) == len(self.frames)

    def _exist_receiver(self, receiver):
        frames = [frame for frame in self.frames if frame.receiver == receiver]
        return len(frames) > 0

    def _get_frame(self, receiver, register):
        for frame in self.frames:
            if frame.receiver == receiver and frame.register == register:
                return frame
