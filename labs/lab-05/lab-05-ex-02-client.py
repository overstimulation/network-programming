#!/usr/bin/env python3
import socket
import sys

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

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, port))
            print(f"[INFO] Connected to {HOST}:{port}")

            while True:
                try:
                    guess = input("Enter your guess: ").strip()
                except EOFError:
                    break

                if not guess:
                    continue

                sock.sendall(guess.encode())
                data = sock.recv(1024)
                if not data:
                    break
                print(f"[INFO] Server response: {data.decode().strip()}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
