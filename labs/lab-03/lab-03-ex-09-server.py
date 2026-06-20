#!/usr/bin/env python3
import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 2906


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        print(
            f"[{timestamp()}] [INFO] UDP reverse DNS server listening on port {PORT}."
        )
        while True:
            data, addr = s.recvfrom(4096)
            ip = data.decode().strip()
            print(f"[{timestamp()}] [INFO] Reverse DNS lookup for '{ip}' from {addr}.")
            try:
                hostname, _, _ = socket.gethostbyaddr(ip)
                response = hostname
            except socket.herror:
                response = "[ERROR] Could not resolve hostname."
            s.sendto(response.encode(), addr)
            print(f"[{timestamp()}] [INFO] Sent to {addr}: '{response}'")


if __name__ == "__main__":
    main()
