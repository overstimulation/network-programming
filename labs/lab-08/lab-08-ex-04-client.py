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
            send_recv(sock, "A2 SELECT INBOX\r\n")
            res = send_recv(sock, "A3 SEARCH UNSEEN\r\n")

            unseen_ids = []
            if res:
                for line in res.split("\r\n"):
                    if line.startswith("* SEARCH"):
                        parts = line.split()
                        if len(parts) > 2:
                            unseen_ids = parts[2:]

            if unseen_ids:
                print(f"[INFO] Found unseen messages: {unseen_ids}")
                tag_idx = 4
                for msg_id in unseen_ids:
                    send_recv(sock, f"A{tag_idx} FETCH {msg_id} BODY[]\r\n")
                    tag_idx += 1
                    send_recv(sock, f"A{tag_idx} STORE {msg_id} +FLAGS \\Seen\r\n")
                    tag_idx += 1
                send_recv(sock, f"A{tag_idx} LOGOUT\r\n")
            else:
                print("[INFO] No unseen messages found.")
                send_recv(sock, "A4 LOGOUT\r\n")
    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
