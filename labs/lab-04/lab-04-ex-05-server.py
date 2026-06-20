#!/usr/bin/env python3
import socket
import sys
from datetime import datetime

HOST = "127.0.0.1"


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    if len(sys.argv) != 2:
        print(f"[ERROR] Usage: {sys.argv[0]} <port>")
        sys.exit(1)
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("[ERROR] Port must be a valid integer.")
        sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))
        print(f"[INFO] UDP reverse DNS server listening on {HOST}:{port}.")
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
