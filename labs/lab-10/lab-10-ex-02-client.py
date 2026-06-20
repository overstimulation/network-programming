#!/usr/bin/env python3
import socket
import os
import base64

HOST = "echo.websocket.org"
PORT = 80


def create_ws_frame(message_bytes):
    frame = bytearray()
    frame.append(0x81)

    msg_len = len(message_bytes)
    frame.append(0x80 | msg_len)

    mask = os.urandom(4)
    frame.extend(mask)

    for i in range(msg_len):
        frame.append(message_bytes[i] ^ mask[i % 4])

    return frame


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
            sock.sendall(request.encode())
            response = sock.recv(4096)

            if b"101 Switching Protocols" in response:
                print("[INFO] Handshake successful!")
                message = b"Hello Server, this is a short message!"
                frame = create_ws_frame(message)
                sock.sendall(frame)
                print(f"[INFO] Sent frame: {message}")
            else:
                print("[ERROR] Handshake failed.")

    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
