#!/usr/bin/env python3
import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 2908
MAX_LEN = 20


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)
    print(
        f"[{timestamp()}] [INFO] TCP fixed-length echo server listening on port {PORT}."
    )

    try:
        while True:
            conn, addr = server.accept()
            print(f"[{timestamp()}] [INFO] Client {addr} connected.")
            try:
                while True:
                    data = conn.recv(MAX_LEN)
                    if not data:
                        print(f"[{timestamp()}] [INFO] Client {addr} disconnected.")
                        break
                    print(
                        f"[{timestamp()}] [INFO] Received from {addr}: '{data.decode()}'"
                    )
                    conn.sendall(data)
            except OSError:
                pass
            finally:
                conn.close()
    finally:
        server.close()


if __name__ == "__main__":
    main()
