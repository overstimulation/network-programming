#!/usr/bin/env python3
import select
import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 2900


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)

    sockets = [server]
    addresses = {}

    print(f"[{timestamp()}] [INFO] TCP echo server listening on port {PORT}.")

    try:
        while True:
            readable, _, _ = select.select(sockets, [], [])
            for sock in readable:
                if sock is server:
                    conn, addr = server.accept()
                    sockets.append(conn)
                    addresses[conn] = addr
                    print(f"[{timestamp()}] [INFO] Client {addr} connected.")
                else:
                    addr = addresses.get(sock)
                    try:
                        data = sock.recv(4096)
                        if data:
                            sock.sendall(data)
                            print(
                                f"[{timestamp()}] [INFO] Echoed {len(data)} bytes to {addr}."
                            )
                        else:
                            print(f"[{timestamp()}] [INFO] Client {addr} disconnected.")
                            sockets.remove(sock)
                            addresses.pop(sock, None)
                            sock.close()
                    except OSError:
                        sockets.remove(sock)
                        addresses.pop(sock, None)
                        sock.close()
    finally:
        server.close()


if __name__ == "__main__":
    main()
