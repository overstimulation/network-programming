#!/usr/bin/env python3
import socket
import sys
import time

HOST = "127.0.0.1"


def send_recv(sock, msg=None):
    if msg:
        print(f"[INFO] Client sending: {msg.strip()}")
        sock.sendall(msg.encode())
    time.sleep(0.1)
    try:
        response = sock.recv(4096).decode()
        for line in response.strip().split("\r\n"):
            print(f"[INFO] Server says: {line}")
        return response
    except socket.timeout:
        return ""


def main():
    if len(sys.argv) != 2:
        print(f"[ERROR] Usage: {sys.argv[0]} <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("[ERROR] Port must be a valid integer.")
        sys.exit(1)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2.0)
            sock.connect((HOST, port))

            send_recv(sock)
            send_recv(sock, "EHLO client\r\n")

            send_recv(sock, "UNKNOWNCMD test\r\n")

            send_recv(sock, "MAIL FROM:<user@test.com>\r\n")
            send_recv(sock, "RCPT TO:<user2@test.com>\r\n")
            send_recv(sock, "DATA\r\n")

            email_body = (
                "From: user@test.com\r\n"
                "To: user2@test.com\r\n"
                "Subject: Final test\r\n"
                "\r\n"
                "Test message.\r\n"
                ".\r\n"
            )
            send_recv(sock, email_body)
            send_recv(sock, "QUIT\r\n")

    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
