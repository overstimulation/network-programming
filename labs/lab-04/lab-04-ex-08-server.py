#!/usr/bin/env python3
import socket
import sys
from datetime import datetime

HOST = "127.0.0.1"
MAX_LEN = 20


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def pad_or_trim(data, length):
    if len(data) < length:
        return data.ljust(length)
    return data[:length]


def recvall(sock, length):
    buffer = b""
    while len(buffer) < length:
        chunk = sock.recv(length - len(buffer))
        if not chunk:
            break
        buffer += chunk
    return buffer


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
    print(f"[INFO] TCP guaranteed fixed-length echo server listening on {HOST}:{port}.")

    try:
        while True:
            conn, addr = server.accept()
            print(f"[INFO] Client {addr} connected.")
            try:
                while True:
                    data = recvall(conn, MAX_LEN)
                    if not data:
                        break
                    response = pad_or_trim(data.decode(), MAX_LEN).encode()
                    conn.sendall(response)
                    print(
                        f"[{timestamp()}] [INFO] Echoed {len(response)} bytes to {addr}."
                    )
            finally:
                conn.close()
                print(f"[INFO] Client {addr} disconnected.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
