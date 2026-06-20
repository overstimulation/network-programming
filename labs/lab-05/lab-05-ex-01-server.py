#!/usr/bin/env python3
import socket
import random

HOST = "127.0.0.1"
PORT = 2912


def main():
    target = random.randint(1, 100)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"[INFO] Mock guessing server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            print(f"[INFO] Client {addr} connected.")
            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    try:
                        guess = int(data.decode().strip())
                        if guess < target:
                            conn.sendall(b"Too small\n")
                        elif guess > target:
                            conn.sendall(b"Too big\n")
                        else:
                            conn.sendall(b"Correct!\n")
                            break
                    except ValueError:
                        conn.sendall(b"Bad input\n")
            finally:
                conn.close()
                print(f"[INFO] Client {addr} disconnected.")
            break


if __name__ == "__main__":
    main()
