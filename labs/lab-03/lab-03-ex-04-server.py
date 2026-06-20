#!/usr/bin/env python3
import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 2901


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        print(f"[{timestamp()}] [INFO] UDP echo server listening on port {PORT}.")
        while True:
            data, addr = s.recvfrom(4096)
            print(
                f"[{timestamp()}] [INFO] Received {len(data)} bytes from {addr}: '{data.decode()}'"
            )
            s.sendto(data, addr)
            print(f"[{timestamp()}] [INFO] Echoed {len(data)} bytes to {addr}.")


if __name__ == "__main__":
    main()
