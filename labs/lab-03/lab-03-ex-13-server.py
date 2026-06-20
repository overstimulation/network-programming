#!/usr/bin/env python3
import socket
from datetime import datetime

HOST = "0.0.0.0"
PORT = 2910


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check_syntax(txt):
    parts = txt.split(";")
    if len(parts) != 7:
        return "BAD_SYNTAX"
    if (
        parts[0] != "zad14odp"
        or parts[1] != "src"
        or parts[3] != "dst"
        or parts[5] != "data"
    ):
        return "BAD_SYNTAX"
    try:
        src_port = int(parts[2])
        dst_port = int(parts[4])
        data = parts[6]
    except ValueError:
        return "BAD_SYNTAX"
    if (
        src_port == 60788
        and dst_port == 2901
        and data == "programming in python is fun"
    ):
        return "TAK"
    return "NIE"


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        print(
            f"[{timestamp()}] [INFO] UDP validation server (zad14odp) listening on port {PORT}."
        )
        while True:
            data, addr = s.recvfrom(1024)
            msg = data.decode()
            print(f"[{timestamp()}] [INFO] Received from {addr}: '{msg}'")
            answer = check_syntax(msg)
            s.sendto(answer.encode(), addr)
            print(f"[{timestamp()}] [INFO] Sent to {addr}: '{answer}'")


if __name__ == "__main__":
    main()
