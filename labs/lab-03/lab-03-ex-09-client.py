#!/usr/bin/env python3
import socket

HOST = "212.182.24.27"
PORT = 2906


def main():
    ip = input("Enter IP address: ")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(5)
            s.sendto(ip.encode(), (HOST, PORT))
            data, _ = s.recvfrom(4096)
            print(f"[INFO] Hostname: {data.decode()}")
    except socket.timeout:
        print(f"[ERROR] No response from {HOST}:{PORT} (timed out).")


if __name__ == "__main__":
    main()
