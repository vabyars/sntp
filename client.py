import socket
import time
import argparse
from packet import SNTP
from config import PORT, SEVENTY_YEARS_IN_SECONDS
import struct


class SntpClient:
    def __init__(self, ntp_server: str):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ntp_server = ntp_server
        self.get_NTP_time()

    def get_NTP_time(self):
        data = SNTP.CLIENT_REQUEST.encode('utf-8')
        self.client.sendto(data, (self.ntp_server, PORT))
        data, address = self.client.recvfrom(1024)
        if data:
            print(f'Response from: {address[0]} : {address[1]}')
        print('\tTime: ' + str(time.ctime(struct.unpack('!12I', data)[10] - SEVENTY_YEARS_IN_SECONDS)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SNTP client')
    parser.add_argument('address', type=str,
                        help='ntp_server to get current time')
    SntpClient(parser.parse_args().address)