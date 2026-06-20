#!/usr/bin/env python3
import socket
import os
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
        sender = input("Sender: ").strip()
        recipient = input("Recipient: ").strip()
        subject = input("Subject: ").strip()
        attachment_path = input("Text attachment path: ").strip()

        print("Body (end with a single dot '.' on a new line):")
        body_lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line == ".":
                break
            body_lines.append(line)

        body = "\r\n".join(body_lines)

        with open(attachment_path, "rb") as f:
            attachment_content = f.read()

        attachment_b64 = base64.b64encode(attachment_content).decode()
        filename = os.path.basename(attachment_path)

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

            send_recv(sock, f"MAIL FROM:<{sender}>\r\n")

            for rcpt in recipient.split(","):
                rcpt = rcpt.strip()
                if rcpt:
                    send_recv(sock, f"RCPT TO:<{rcpt}>\r\n")

            send_recv(sock, "DATA\r\n")

            email_data = (
                f"From: {sender}\r\n"
                f"To: {recipient}\r\n"
                f"Subject: {subject}\r\n"
                "MIME-Version: 1.0\r\n"
                "Content-Type: multipart/mixed; boundary=sep\r\n"
                "\r\n"
                "--sep\r\n"
                "Content-Type: text/plain; charset=UTF-8\r\n"
                "\r\n"
                f"{body}\r\n"
                "--sep\r\n"
                f'Content-Type: text/plain; name="{filename}"\r\n'
                f'Content-Disposition: attachment; filename="{filename}"\r\n'
                "Content-Transfer-Encoding: base64\r\n"
                "\r\n"
                f"{attachment_b64}\r\n"
                "--sep--\r\n"
                ".\r\n"
            )
            send_recv(sock, email_data)
            send_recv(sock, "QUIT\r\n")

    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
