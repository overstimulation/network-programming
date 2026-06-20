#!/usr/bin/env python3
import socket
import sys
from datetime import datetime

HOST = "127.0.0.1"


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check_msg_a(txt):
    parts = txt.split(";")
    if len(parts) != 9:
        return "BAD_SYNTAX"
    if (
        parts[0] != "zad15odpA"
        or parts[1] != "ver"
        or parts[3] != "srcip"
        or parts[5] != "dstip"
        or parts[7] != "type"
    ):
        return "BAD_SYNTAX"
    try:
        ver = int(parts[2])
        src_ip = parts[4]
        dst_ip = parts[6]
        proto = int(parts[8])
    except ValueError:
        return "BAD_SYNTAX"
    if (
        ver == 4
        and proto == 6
        and src_ip == "212.182.24.27"
        and dst_ip == "192.168.0.2"
    ):
        return "TAK"
    return "NIE"


def check_msg_b(txt):
    parts = txt.split(";")
    if len(parts) != 7:
        return "BAD_SYNTAX"
    if (
        parts[0] != "zad15odpB"
        or parts[1] != "srcport"
        or parts[3] != "dstport"
        or parts[5] != "data"
    ):
        return "BAD_SYNTAX"
    try:
        src_port = int(parts[2])
        dst_port = int(parts[4])
        data = parts[6]
    except ValueError:
        return "BAD_SYNTAX"
    if src_port == 2900 and dst_port == 47526 and data == "network programming is fun":
        return "TAK"
    return "NIE"


def main():
    if len(sys.argv) != 2:
        print(f"[ERROR] Usage: {sys.argv[0]} <port>")
        sys.exit(1)
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("[ERROR] Port must be a valid integer.")
        sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))
        print(
            f"[INFO] UDP validation server (ex-15 protocol) listening on {HOST}:{port}."
        )
        while True:
            data, addr = s.recvfrom(1024)
            msg = data.decode()
            print(f"[{timestamp()}] [INFO] Received from {addr}: '{msg}'")
            prefix = msg.split(";")[0]
            if prefix == "zad15odpA":
                answer = check_msg_a(msg)
            elif prefix == "zad15odpB":
                answer = check_msg_b(msg)
            else:
                answer = "BAD_SYNTAX"
            s.sendto(answer.encode(), addr)
            print(f"[{timestamp()}] [INFO] Sent to {addr}: '{answer}'")


if __name__ == "__main__":
    main()
