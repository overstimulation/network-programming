#!/usr/bin/env python3
import socket

HOST = "212.182.24.27"
PORT = 2901


def main():
    message = input("Enter message to send: ")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(5)
            s.sendto(message.encode(), (HOST, PORT))
            data, _ = s.recvfrom(4096)
            print(f"[INFO] Server response: {data.decode()}")
    except socket.timeout:
        print(f"[ERROR] No response from {HOST}:{PORT} (timed out).")


if __name__ == "__main__":
    main()
