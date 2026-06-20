#!/usr/bin/env python3
import socket
import sys
from datetime import datetime

HOST = "127.0.0.1"


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    if len(sys.argv) != 2:
        print(f"[ERROR] Usage: {sys.argv[0]} <port>")
        sys.exit(1)
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("[ERROR] Port must be a valid integer.")
        sys.exit(1)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, port))
    server.listen(1)
    print(f"[INFO] TCP echo server listening on {HOST}:{port}.")

    try:
        while True:
            conn, addr = server.accept()
            print(f"[INFO] Client {addr} connected.")
            try:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    conn.sendall(data)
                    print(f"[{timestamp()}] [INFO] Echoed {len(data)} bytes to {addr}.")
            finally:
                conn.close()
                print(f"[INFO] Client {addr} disconnected.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
