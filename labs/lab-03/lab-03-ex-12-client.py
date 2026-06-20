#!/usr/bin/env python3
import socket

HOST = "212.182.24.27"
PORT = 2908
MAX_LEN = 20


def pad_or_trim(message, length):
    if len(message) < length:
        return message.ljust(length)
    return message[:length]


def recvall(sock, length):
    buffer = b""
    while len(buffer) < length:
        chunk = sock.recv(length - len(buffer))
        if not chunk:
            break
        buffer += chunk
    return buffer


def main():
    message = input("Enter message (up to 20 chars): ")
    prepared = pad_or_trim(message, MAX_LEN)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((HOST, PORT))
            s.sendall(prepared.encode())
            print(f"[INFO] Sent:     '{prepared}'")
            response = recvall(s, MAX_LEN)
            print(f"[INFO] Received: '{response.decode()}'")
    except socket.timeout:
        print(f"[ERROR] Connection to {HOST}:{PORT} timed out.")
    except ConnectionRefusedError:
        print(f"[ERROR] Connection to {HOST}:{PORT} refused.")


if __name__ == "__main__":
    main()
