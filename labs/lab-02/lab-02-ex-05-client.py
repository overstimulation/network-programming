#!/usr/bin/env python3
import socket

HOST = "212.182.24.27"
PORT = 2901


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(5)
            print(
                f"[INFO] UDP client ready. Sending to {HOST}:{PORT}. Type your message (Ctrl+D to quit)."
            )
            while True:
                try:
                    message = input("> ")
                except EOFError:
                    break
                if not message:
                    continue
                s.sendto(message.encode(), (HOST, PORT))
                data, _ = s.recvfrom(4096)
                print(f"[INFO] Server: {data.decode()}")
    except socket.timeout:
        print(f"[ERROR] No response from {HOST}:{PORT} (timed out).")


if __name__ == "__main__":
    main()
