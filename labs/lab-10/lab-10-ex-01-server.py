#!/usr/bin/env python3
import socket
import os
import base64
import hashlib

HOST = "127.0.0.1"
PORT = int(os.environ.get("HTTP_PORT", 8080))
WS_MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(1)
            print(f"[INFO] Server listening on {HOST}:{PORT}")

            conn, addr = server.accept()
            with conn:
                data = conn.recv(4096)
                request = data.decode(errors="ignore")

                ws_key = None
                for line in request.split("\r\n"):
                    if line.lower().startswith("sec-websocket-key:"):
                        ws_key = line.split(":", 1)[1].strip()
                        break

                if ws_key:
                    accept_key = base64.b64encode(
                        hashlib.sha1((ws_key + WS_MAGIC_STRING).encode()).digest()
                    ).decode()

                    response = (
                        "HTTP/1.1 101 Switching Protocols\r\n"
                        "Upgrade: websocket\r\n"
                        "Connection: Upgrade\r\n"
                        f"Sec-WebSocket-Accept: {accept_key}\r\n"
                        "\r\n"
                    )
                    conn.sendall(response.encode())
                    print("[INFO] Sent handshake response.")
                else:
                    print("[ERROR] No Sec-WebSocket-Key found.")

    except Exception as e:
        print(f"[ERROR] Server error: {e}")


if __name__ == "__main__":
    main()
