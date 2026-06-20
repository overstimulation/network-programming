#!/usr/bin/env python3
import socket
import os
import base64
import hashlib

HOST = "127.0.0.1"
PORT = int(os.environ.get("HTTP_PORT", 8080))
WS_MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def unmask_payload(payload, mask):
    unmasked = bytearray()
    for i in range(len(payload)):
        unmasked.append(payload[i] ^ mask[i % 4])
    return unmasked


def create_server_frame(message_bytes):
    frame = bytearray()
    frame.append(0x81)

    msg_len = len(message_bytes)
    if msg_len <= 125:
        frame.append(msg_len)
    elif msg_len <= 65535:
        frame.append(126)
        frame.append((msg_len >> 8) & 0xFF)
        frame.append(msg_len & 0xFF)
    else:
        frame.append(127)
        for i in range(7, -1, -1):
            frame.append((msg_len >> (i * 8)) & 0xFF)

    frame.extend(message_bytes)
    return frame


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

                    while True:
                        frame_header = conn.recv(2)
                        if not frame_header:
                            break
                        if len(frame_header) < 2:
                            break

                        opcode = frame_header[0] & 0x0F
                        if opcode == 8:
                            print("[INFO] Received close frame.")
                            break

                        payload_len = frame_header[1] & 0x7F
                        is_masked = bool(frame_header[1] & 0x80)

                        if payload_len == 126:
                            ext_len = conn.recv(2)
                            payload_len = (ext_len[0] << 8) | ext_len[1]
                        elif payload_len == 127:
                            ext_len = conn.recv(8)
                            payload_len = 0
                            for i in range(8):
                                payload_len = (payload_len << 8) | ext_len[i]

                        if is_masked:
                            mask = conn.recv(4)
                            payload = bytearray()
                            while len(payload) < payload_len:
                                chunk = conn.recv(min(4096, payload_len - len(payload)))
                                if not chunk:
                                    break
                                payload.extend(chunk)

                            message = unmask_payload(payload, mask)
                            print(f"[INFO] Received message of length: {len(message)}")

                            response_frame = create_server_frame(message)
                            conn.sendall(response_frame)
                            print(f"[INFO] Sent echo of length: {len(message)}")
                        else:
                            print("[ERROR] Frame is not masked.")
                            break
                else:
                    print("[ERROR] No Sec-WebSocket-Key found.")

    except Exception as e:
        print(f"[ERROR] Server error: {e}")


if __name__ == "__main__":
    main()
