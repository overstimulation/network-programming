#!/usr/bin/env python3
import socket
import sys
import random

HOST = "127.0.0.1"


def main():
    if len(sys.argv) != 2:
        print(f"[ERROR] Usage: {sys.argv[0]} <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("[ERROR] Port must be a valid integer.")
        sys.exit(1)

    target_number = random.randint(1, 100)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, port))
        server.listen(1)
        print(f"[INFO] Guessing server listening on {HOST}:{port}")

        conn, addr = server.accept()
        print(f"[INFO] Client {addr} connected.")
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                try:
                    guess = int(data.decode().strip())
                except ValueError:
                    conn.sendall(b"Error: input is not a number\n")
                    continue

                if guess < target_number:
                    conn.sendall(b"Smaller than target\n")
                elif guess > target_number:
                    conn.sendall(b"Bigger than target\n")
                else:
                    conn.sendall(b"Equal to target. You win!\n")
                    break
        finally:
            conn.close()
            print(f"[INFO] Client {addr} disconnected. Server terminating.")


if __name__ == "__main__":
    main()
