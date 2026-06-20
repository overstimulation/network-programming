#!/usr/bin/env python3
import socket
import time

HOST = "212.182.24.27"
PORT = 143


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
            send_recv(sock, "A1 LOGIN pasumcs@infumcs.edu P4SInf2017\r\n")
            res = send_recv(sock, "A2 STATUS INBOX (MESSAGES)\r\n")

            if res:
                for line in res.split("\r\n"):
                    if line.startswith("* STATUS"):
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if "MESSAGES" in part.upper() and i + 1 < len(parts):
                                num = parts[i + 1].strip(")")
                                print(f"[INFO] Number of messages in Inbox: {num}")

            send_recv(sock, "A3 LOGOUT\r\n")
    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
