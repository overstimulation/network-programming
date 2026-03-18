#!/usr/bin/env python3
import sys
import socket


def main():
    if len(sys.argv) != 2:
        print(f"[ERROR] Usage: {sys.argv[0]} <ip_address>")
        sys.exit(1)

    ip_address = sys.argv[1]

    try:
        host_info = socket.gethostbyaddr(ip_address)
        hostname = host_info[0]
        print(f"[INFO] The hostname for {ip_address} is {hostname}")

    except Exception as error:
        print(f"[ERROR] Could not resolve hostname: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
