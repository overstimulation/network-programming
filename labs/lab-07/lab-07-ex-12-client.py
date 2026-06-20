#!/usr/bin/env python3
import socket
import time

HOST = "127.0.0.1"
PORT = 1100


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
            send_recv(sock, "UNKNOWN\r\n")
            send_recv(sock, "USER pas2017@interia.pl\r\n")
            send_recv(sock, "PASS P4SInf2017\r\n")
            send_recv(sock, "STAT\r\n")
            send_recv(sock, "LIST\r\n")
            send_recv(sock, "RETR 1\r\n")
            send_recv(sock, "DELE 1\r\n")
            send_recv(sock, "QUIT\r\n")
    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
