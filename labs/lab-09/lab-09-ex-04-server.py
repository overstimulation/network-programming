#!/usr/bin/env python3
import socket
import os

HOST = "127.0.0.1"
PORT = int(os.environ.get("HTTP_PORT", 8080))


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(1)
            print(f"[INFO] Server listening on {HOST}:{PORT}")

            conn, addr = server.accept()
            with conn:
                print(f"[INFO] Accepted connection from {addr}")
                data = conn.recv(4096)
                if data:
                    print(
                        f"[INFO] Request headers and body:\n{data.decode(errors='ignore')}"
                    )

                body = b'{"status": "success"}'
                response = (
                    b"HTTP/1.1 200 OK\r\n"
                    b"Content-Type: application/json\r\n"
                    b"Connection: close\r\n"
                    + f"Content-Length: {len(body)}\r\n".encode()
                    + b"\r\n"
                    + body
                )
                conn.sendall(response)

    except Exception as e:
        print(f"[ERROR] Server error: {e}")


if __name__ == "__main__":
    main()
