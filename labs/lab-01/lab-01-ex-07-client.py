#!/usr/bin/env python3
import sys
import socket

MIN_PORT = 1
MAX_PORT = 1024


def main():
    if len(sys.argv) != 2:
        print(f"[ERROR] Usage: {sys.argv[0]} <host>")
        sys.exit(1)

    host = sys.argv[1]
    print(f"[INFO] Scanning ports {MIN_PORT}-{MAX_PORT} on {host}...")

    for port in range(MIN_PORT, MAX_PORT + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.3)
                sock.connect((host, port))
                print(f"[INFO] Port {port} is OPEN")
        except Exception:
            pass

    print("[INFO] Scan finished.")


if __name__ == "__main__":
    main()
