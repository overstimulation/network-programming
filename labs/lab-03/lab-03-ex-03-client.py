#!/usr/bin/env python3
import socket

HOST = "212.182.24.27"
PORT = 2900


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((HOST, PORT))
            print(
                f"[INFO] Connected to {HOST}:{PORT}. Type your message (Ctrl+D to quit)."
            )
            while True:
                try:
                    message = input("> ")
                except EOFError:
                    break
                if not message:
                    continue
                s.sendall(message.encode())
                response = s.recv(4096)
                print(f"[INFO] Server: {response.decode()}")
    except socket.timeout:
        print(f"[ERROR] Connection to {HOST}:{PORT} timed out.")
    except ConnectionRefusedError:
        print(f"[ERROR] Connection to {HOST}:{PORT} refused.")


if __name__ == "__main__":
    main()
