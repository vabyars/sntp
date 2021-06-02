import argparse
import socket
from packet import SNTP
from config import PORT, IP, BUFFER_SIZE


class Server:
    def __init__(self, dt):
        self.delta = dt
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((IP, PORT))
        print(f'Server start on {IP}:{PORT}')

    def run(self):
        while True:
            received_packet, address = self.server.recvfrom(BUFFER_SIZE)
            sntp = SNTP(self.delta)
            sntp.analise_packet(received_packet)
            packet = sntp.get_server_packet()
            self.server.sendto(packet, address)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SNTP server with wrong time')
    parser.add_argument('-o', '--offset', action='store', default=200000, type=int,
                        dest='time_offset', help='Time offset')
    Server(parser.parse_args().time_offset).run()