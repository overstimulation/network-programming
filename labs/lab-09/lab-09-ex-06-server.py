#!/usr/bin/env python3
import socket
import os
import base64

HOST = "127.0.0.1"
PORT = int(os.environ.get("HTTP_PORT", 8080))


def main():
    try:
        b64_img = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
        body = base64.b64decode(b64_img)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(1)
            print(f"[INFO] Server listening on {HOST}:{PORT}")

            conn, addr = server.accept()
            with conn:
                data = conn.recv(4096)
                if not data:
                    return

                req = data.decode(errors="ignore")
                modified_since = None
                for line in req.split("\r\n"):
                    if line.lower().startswith("if-modified-since:"):
                        modified_since = line.split(":", 1)[1].strip()

                if modified_since:
                    response = b"HTTP/1.1 304 Not Modified\r\nConnection: close\r\n\r\n"
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

    except Exception as e:
        print(f"[ERROR] Server error: {e}")


if __name__ == "__main__":
    main()
