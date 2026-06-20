#!/usr/bin/env python3
import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 2907


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        print(f"[{timestamp()}] [INFO] UDP DNS server listening on port {PORT}.")
        while True:
            data, addr = s.recvfrom(4096)
            hostname = data.decode().strip()
            print(f"[{timestamp()}] [INFO] DNS lookup for '{hostname}' from {addr}.")
            try:
                ip = socket.gethostbyname(hostname)
                response = ip
            except socket.gaierror:
                response = "[ERROR] Could not resolve IP address."
            s.sendto(response.encode(), addr)
            print(f"[{timestamp()}] [INFO] Sent to {addr}: '{response}'")


if __name__ == "__main__":
    main()
