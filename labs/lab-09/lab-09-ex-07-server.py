#!/usr/bin/env python3
import socket
import os

HOST = "127.0.0.1"
PORT = int(os.environ.get("HTTP_PORT", 8080))


def handle_client(conn, addr):
    try:
        data = conn.recv(4096)
        if not data:
            return

        request = data.decode(errors="ignore")
        lines = request.split("\r\n")
        if not lines:
            return

        first_line = lines[0].split()
        if len(first_line) < 2:
            return

        method = first_line[0]
        path = first_line[1]

        print(f"[INFO] {addr} requested {method} {path}")

        if method != "GET":
            response = (
                "HTTP/1.1 405 Method Not Allowed\r\n"
                "Connection: close\r\n"
                "\r\n"
                "Method Not Allowed"
            )
            conn.sendall(response.encode())
            return

        if path == "/" or path == "/index.html":
            body = "<html><body><h1>Welcome to Lab 09 Server</h1></body></html>"
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(body)}\r\n"
                "Connection: close\r\n"
                "\r\n"
                f"{body}"
            )
            conn.sendall(response.encode())
        else:
            body = "<html><body><h1>404 Not Found</h1></body></html>"
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(body)}\r\n"
                "Connection: close\r\n"
                "\r\n"
                f"{body}"
            )
            conn.sendall(response.encode())

    except Exception as e:
        print(f"[ERROR] Error handling client: {e}")
    finally:
        conn.close()


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(5)
            print(f"[INFO] HTTP Server listening on {HOST}:{PORT}")

            conn, addr = server.accept()
            handle_client(conn, addr)

            conn, addr = server.accept()
            handle_client(conn, addr)

    except Exception as e:
        print(f"[ERROR] Server error: {e}")


if __name__ == "__main__":
    main()
