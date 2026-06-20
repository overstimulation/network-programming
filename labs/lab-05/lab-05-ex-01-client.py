#!/usr/bin/env python3
import socket

HOST = "212.182.24.27"
PORT = 2912


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            print(f"[INFO] Connected to {HOST}:{PORT}")

            while True:
                try:
                    guess = input("Enter your guess: ").strip()
                except EOFError:
                    break

                if not guess:
                    continue

                sock.sendall(guess.encode())
                response = sock.recv(1024).decode().strip()
                if not response:
                    break

                print(f"[INFO] Server response: {response}")

    except ConnectionRefusedError:
        print(f"[ERROR] Connection to {HOST}:{PORT} refused.")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
