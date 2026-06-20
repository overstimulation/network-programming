#!/usr/bin/env python3
import socket
import os
import base64

HOST = "127.0.0.1"
PORT = int(os.environ.get("HTTP_PORT", 8080))


def handle_client(conn, b64_img):
    data = conn.recv(4096)
    if not data:
        return

    req = data.decode(errors="ignore")
    range_header = None
    for line in req.split("\r\n"):
        if line.lower().startswith("range: bytes="):
            range_header = line.split("=")[1].strip()

    body = base64.b64decode(b64_img)
    if range_header:
        parts = range_header.split("-")
        start = int(parts[0]) if parts[0] else 0
        end = int(parts[1]) if len(parts) > 1 and parts[1] else len(body) - 1

        chunk = body[start : end + 1]
        response = (
            b"HTTP/1.1 206 Partial Content\r\n"
            b"Content-Type: image/jpeg\r\n"
            + f"Content-Range: bytes {start}-{end}/{len(body)}\r\n".encode()
            + b"Connection: close\r\n"
            + f"Content-Length: {len(chunk)}\r\n".encode()
            + b"\r\n"
            + chunk
        )
    else:
        response = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: image/jpeg\r\n"
            b"Connection: close\r\n"
            + f"Content-Length: {len(body)}\r\n".encode()
            + b"\r\n"
            + body
        )
    conn.sendall(response)


def main():
    try:
        b64_img = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(5)
            print(f"[INFO] Server listening on {HOST}:{PORT}")

            for _ in range(3):
                conn, addr = server.accept()
                with conn:
                    handle_client(conn, b64_img)

    except Exception as e:
        print(f"[ERROR] Server error: {e}")


if __name__ == "__main__":
    main()
