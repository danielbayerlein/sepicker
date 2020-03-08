import logging

LOGGER = logging.getLogger(__name__)


class ElsterFrame:
    READ = 0x1

    def __init__(self, name, index, format=None):
        receiver, register = str(index).split('.')
        self.name = name
        self.receiver = int(receiver, 16)
        self.register = int(register, 16)
        self.format = format

    def message(self):
        msg = [0] * 5
        msg[0] = (self.READ & 0xf) | ((self.receiver >> 3) & 0xf0)
        msg[1] = self.receiver & 0x7f
        msg[2] = 0xfa
        msg[3] = self.register >> 8
        msg[4] = self.register & 0xff

        return msg

    def formatter(self, value):
        if not self.format:
            return value

        return {
            'dec_val': '{0:.1f}'.format(value / 10.0),
            'mil_val': '{0:.3f}'.format(value / 1000.0),
            'little_endian': '{:d}'.format((value >> 8) + 256 * (value & 0xff))
        }[self.format]
