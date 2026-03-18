#!/usr/bin/env python3
import sys
import socket


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

    try:
        with socket.socket() as sock:
            sock.connect((host, port))
            print(f"[INFO] Successfully connected to {host}:{port}")
    except Exception as error:
        print(f"[ERROR] Failed to connect to {host}:{port}: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
