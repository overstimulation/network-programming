#!/usr/bin/env python3
import sys
import socket


def main():
    if len(sys.argv) != 2:
        print(f"[ERROR] Usage: {sys.argv[0]} <hostname>")
        sys.exit(1)

    hostname = sys.argv[1]

    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"[INFO] The IP address for {hostname} is {ip_address}")
    except Exception as error:
        print(f"[ERROR] Could not resolve hostname '{hostname}': {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
