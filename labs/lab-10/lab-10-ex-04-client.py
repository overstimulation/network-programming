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
    if msg_len <= 125:
        frame.append(0x80 | msg_len)
    elif msg_len <= 65535:
        frame.append(0x80 | 126)
        frame.append((msg_len >> 8) & 0xFF)
        frame.append(msg_len & 0xFF)
    else:
        frame.append(0x80 | 127)
        for i in range(7, -1, -1):
            frame.append((msg_len >> (i * 8)) & 0xFF)

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

                message = b"Echo Test Message"
                frame = create_ws_frame(message)
                sock.sendall(frame)
                print(f"[INFO] Sent frame: {message}")

                resp_header = sock.recv(2)
                if len(resp_header) == 2:
                    payload_len = resp_header[1] & 0x7F
                    if payload_len == 126:
                        ext_len = sock.recv(2)
                        payload_len = (ext_len[0] << 8) | ext_len[1]
                    elif payload_len == 127:
                        ext_len = sock.recv(8)
                        payload_len = 0
                        for i in range(8):
                            payload_len = (payload_len << 8) | ext_len[i]

                    payload = bytearray()
                    while len(payload) < payload_len:
                        chunk = sock.recv(min(4096, payload_len - len(payload)))
                        if not chunk:
                            break
                        payload.extend(chunk)

                    print(f"[INFO] Received echo: {payload.decode(errors='ignore')}")

                close_frame = bytearray([0x88, 0x80])
                mask = os.urandom(4)
                close_frame.extend(mask)
                sock.sendall(close_frame)

            else:
                print("[ERROR] Handshake failed.")

    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
