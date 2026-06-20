#!/usr/bin/env python3
import socket
import sys

MIN_PORT = 1
MAX_PORT = 1024


def get_service(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"


def main():
    if len(sys.argv) != 2:
        print(f"[ERROR] Usage: {sys.argv[0]} <host>")
        sys.exit(1)

    host = sys.argv[1]
    print(f"[INFO] Scanning ports {MIN_PORT}-{MAX_PORT} on {host}...")

    for port in range(MIN_PORT, MAX_PORT + 1):
        service = get_service(port)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                s.connect((host, port))
                print(f"[INFO] Port {port}/tcp is OPEN (service: {service})")
        except Exception:
            print(f"[INFO] Port {port}/tcp is CLOSED (service: {service})")

    print("[INFO] Scan complete.")


if __name__ == "__main__":
    main()
