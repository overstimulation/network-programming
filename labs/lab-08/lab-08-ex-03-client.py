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
            res = send_recv(sock, 'A2 LIST "" *\r\n')

            mailboxes = []
            if res:
                for line in res.split("\r\n"):
                    if line.startswith("* LIST"):
                        parts = line.split('"/"')
                        if len(parts) == 2:
                            mailboxes.append(parts[1].strip())

            total_msgs = 0
            for i, mb in enumerate(mailboxes):
                tag = f"A{3 + i}"
                st_res = send_recv(sock, f"{tag} STATUS {mb} (MESSAGES)\r\n")
                if st_res:
                    for line in st_res.split("\r\n"):
                        if line.startswith("* STATUS"):
                            parts = line.split()
                            for j, part in enumerate(parts):
                                if "MESSAGES" in part.upper() and j + 1 < len(parts):
                                    num = int(parts[j + 1].strip(")"))
                                    total_msgs += num

            print(f"[INFO] Total messages across all mailboxes: {total_msgs}")

            tag_logout = f"A{3 + len(mailboxes)}"
            send_recv(sock, f"{tag_logout} LOGOUT\r\n")
    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
