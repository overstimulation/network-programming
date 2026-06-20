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
            res = send_recv(sock, "LIST\r\n")

            max_size = -1
            max_id = -1

            if res:
                lines = res.split("\r\n")
                for line in lines[1:]:
                    if line == "." or not line:
                        break
                    parts = line.split()
                    if len(parts) == 2:
                        msg_id = int(parts[0])
                        size = int(parts[1])
                        if size > max_size:
                            max_size = size
                            max_id = msg_id

            if max_id != -1:
                print(f"[INFO] Largest message is {max_id} with size {max_size}")
                send_recv(sock, f"RETR {max_id}\r\n")

            send_recv(sock, "QUIT\r\n")
    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
