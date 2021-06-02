import struct
from decimal import Decimal
import time
from config import SEVENTY_YEARS_IN_SECONDS, BITE_OFFSET


class SNTP:
    HEADER_FORMAT = '> B B B B I I 4s Q Q Q Q'
    LEAP_INDICATOR = 0
    VERSION_NUMBER = 4
    MODE = 4
    STRATUM = 1
    FIRST_OCTET = LEAP_INDICATOR << 6 | VERSION_NUMBER << 3 | MODE
    CLIENT_REQUEST = '\x1b' + 47 * '\0'

    def __init__(self, time_delta=0):
        self.received_time = self.get_wrong_time()
        self.transmit_time = 0
        self.time_delta = time_delta

    def analise_packet(self, received_packet):
        self.transmit_time = struct.unpack(self.HEADER_FORMAT, received_packet)[10]

    def get_server_packet(self):
        return struct.pack(self.HEADER_FORMAT, self.FIRST_OCTET,
                           self.STRATUM, 0, 0, 0, 0, b'', 0,
                           self.transmit_time, self.received_time,
                           self.get_wrong_time(self.time_delta))

    def get_wrong_time(self, time_delta=0):
        now = time.time() + SEVENTY_YEARS_IN_SECONDS
        wrong_time = now + time_delta
        return int(Decimal(wrong_time) * BITE_OFFSET)