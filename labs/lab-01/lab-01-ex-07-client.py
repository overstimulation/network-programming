#!/usr/bin/env python3
import sys
import socket


def main():
    if len(sys.argv) != 2:
        print(f"[ERROR] Usage: {sys.argv[0]} <host>")
        sys.exit(1)

    host = sys.argv[1]
    print(f"[INFO] Scanning ports 1-1024 on {host}...")

    for port in range(1, 1025):
        try:
            with socket.socket() as sock:
                sock.settimeout(0.3)
                sock.connect((host, port))
                print(f"[+] Port {port} is OPEN")
        except Exception:
            pass

    print("[INFO] Scan finished.")


if __name__ == "__main__":
    main()
