#!/usr/bin/env python3
import socket
import time

HOST = "interia.pl"
PORT = 110


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
            send_recv(sock, "USER pas2017@interia.pl\r\n")
            send_recv(sock, "PASS P4SInf2017\r\n")
            res = send_recv(sock, "STAT\r\n")
            if res and res.startswith("+OK"):
                parts = res.split()
                if len(parts) >= 3:
                    print(f"[INFO] Total bytes: {parts[2]}")
            send_recv(sock, "QUIT\r\n")
    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
