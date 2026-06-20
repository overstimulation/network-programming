#!/usr/bin/env python3
import socket
import sys


def get_service(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"


def main():
    if len(sys.argv) != 3:
        print(f"[ERROR] Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("[ERROR] Port must be a valid integer.")
        sys.exit(1)

    service = get_service(port)
    try:
        with socket.socket() as s:
            s.settimeout(1)
            s.connect((host, port))
            print(f"[INFO] Port {port}/tcp is OPEN (service: {service})")
    except (ConnectionRefusedError, socket.timeout, OSError):
        print(f"[INFO] Port {port}/tcp is CLOSED (service: {service})")


if __name__ == "__main__":
    main()
