#!/usr/bin/env python3
import socket
import os
import base64

HOST = "echo.websocket.org"
PORT = 80


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5.0)
            sock.connect((HOST, PORT))

            key = base64.b64encode(os.urandom(16)).decode()
            request = (
                "GET / HTTP/1.1\r\n"
                f"Host: {HOST}:{PORT}\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {key}\r\n"
                "Sec-WebSocket-Version: 13\r\n"
                "\r\n"
            )
            print("[INFO] Sending handshake request...")
            sock.sendall(request.encode())

            response = sock.recv(4096)
            print(
                f"[INFO] Received handshake response:\n{response.decode(errors='ignore')}"
            )

            if b"101 Switching Protocols" in response:
                print("[INFO] Handshake successful!")
            else:
                print("[ERROR] Handshake failed.")

    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
