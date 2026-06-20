#!/usr/bin/env python3
import socket
import base64
import time

HOST = "interia.pl"
PORT = 587


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
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2.0)
            sock.connect((HOST, PORT))

            send_recv(sock)
            send_recv(sock, "EHLO myclient\r\n")
            send_recv(sock, "AUTH LOGIN\r\n")

            user_b64 = base64.b64encode(b"pas2017@interia.pl").decode()
            send_recv(sock, f"{user_b64}\r\n")

            pass_b64 = base64.b64encode(b"P4SInf2017").decode()
            send_recv(sock, f"{pass_b64}\r\n")

            send_recv(sock, "MAIL FROM:<pas2017@interia.pl>\r\n")
            send_recv(sock, "RCPT TO:<pas2017@interia.pl>\r\n")
            send_recv(sock, "RCPT TO:<pasinf2017@interia.pl>\r\n")
            send_recv(sock, "DATA\r\n")

            email_body = (
                "From: pas2017@interia.pl\r\n"
                "To: pas2017@interia.pl, pasinf2017@interia.pl\r\n"
                "Subject: Test email from ex-02 (Multiple recipients)\r\n"
                "\r\n"
                "Hello, this is a test message to multiple recipients.\r\n"
                ".\r\n"
            )
            send_recv(sock, email_body)
            send_recv(sock, "QUIT\r\n")

    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
