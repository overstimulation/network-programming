#!/usr/bin/env python3
import socket

HOST = "212.182.24.27"
PORT = 2900


def main():
    message = input("Enter message to send: ")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((HOST, PORT))
            s.sendall(message.encode())
            response = s.recv(4096)
            print(f"[INFO] Server response: {response.decode()}")
    except socket.timeout:
        print(f"[ERROR] Connection to {HOST}:{PORT} timed out.")
    except ConnectionRefusedError:
        print(f"[ERROR] Connection to {HOST}:{PORT} refused.")


if __name__ == "__main__":
    main()
