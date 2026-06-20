#!/usr/bin/env python3
import socket
import sys
import threading

HOST = "127.0.0.1"


def tcp_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))
        s.listen(1)
        print(f"[INFO] TCP server listening on {HOST}:{port}")
        while True:
            conn, addr = s.accept()
            try:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    conn.sendall(data)
            finally:
                conn.close()


def udp_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))
        print(f"[INFO] UDP server listening on {HOST}:{port}")
        while True:
            data, addr = s.recvfrom(4096)
            s.sendto(data, addr)


def main():
    if len(sys.argv) != 3:
        print(f"[ERROR] Usage: {sys.argv[0]} <tcp_port> <udp_port>")
        sys.exit(1)

    try:
        tcp_port = int(sys.argv[1])
        udp_port = int(sys.argv[2])
    except ValueError:
        print("[ERROR] Ports must be valid integers.")
        sys.exit(1)

    t1 = threading.Thread(target=tcp_server, args=(tcp_port,), daemon=True)
    t2 = threading.Thread(target=udp_server, args=(udp_port,), daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
