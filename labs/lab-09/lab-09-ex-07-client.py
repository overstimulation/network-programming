#!/usr/bin/env python3
import socket

HOST = "127.0.0.1"
PORT = 8080


def fetch(path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5.0)
        sock.connect((HOST, PORT))

        request = f"GET {path} HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n"
        print(f"[INFO] Sending request for {path}")
        sock.sendall(request.encode())

        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk

        print(f"[INFO] Response:\n{response.decode(errors='ignore')}")


def main():
    try:
        fetch("/")
        fetch("/missing.html")
    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
