#!/usr/bin/env python3
import socket
import threading

HOST = "127.0.0.1"
TCP_PORT = 2913
UDP_PORTS = [666, 1666, 2666]


def udp_listener(port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))
        while True:
            data, addr = s.recvfrom(1024)
            if data.decode().strip() == "PING":
                s.sendto(b"PONG", addr)


def main():
    for port in UDP_PORTS:
        t = threading.Thread(target=udp_listener, args=(port,), daemon=True)
        t.start()

    print(f"[INFO] Mock hidden TCP service waiting on {HOST}:{TCP_PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, TCP_PORT))
        s.listen(1)

        while True:
            conn, addr = s.accept()
            print(f"[INFO] Connection accepted from {addr}")
            try:
                conn.sendall(b"Congratulations! You found the hidden.\n")
            finally:
                conn.close()
            break


if __name__ == "__main__":
    main()
