#!/usr/bin/env python3
import sys
import socket


def main():
    if len(sys.argv) != 3:
        print(f"[ERROR] Usage: {sys.argv[0]} <host> <port>")
        sys.exit(1)

    host = sys.argv[1]

    try:
        port = int(sys.argv[2])
    except ValueError:
        print("[ERROR] Port must be a valid integer.")
        sys.exit(1)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind((host, port))
            server_sock.listen(1)
            print(f"[INFO] Server listening on {host}:{port}")

            client_sock, client_addr = server_sock.accept()
            with client_sock:
                print(f"[INFO] Accepted connection from {client_addr}")

    except Exception as error:
        print(f"[ERROR] Server failed: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
