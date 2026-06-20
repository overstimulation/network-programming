#!/usr/bin/env python3
import socket
import sys
from datetime import datetime

HOST = "127.0.0.1"


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate(num1, op, num2):
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        if num2 == 0:
            raise ZeroDivisionError("division by zero")
        return num1 / num2
    raise ValueError(f"unsupported operator: '{op}'")


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
        print(f"[INFO] UDP calculator server listening on {HOST}:{port}.")
        while True:
            data, addr = s.recvfrom(4096)
            message = data.decode().strip()
            print(f"[{timestamp()}] [INFO] Received from {addr}: '{message}'")
            try:
                parts = message.split()
                if len(parts) != 3:
                    raise ValueError("expected format: num1 op num2")
                num1, op, num2 = float(parts[0]), parts[1], float(parts[2])
                result = calculate(num1, op, num2)
                response = str(result)
            except (ValueError, ZeroDivisionError) as e:
                response = f"[ERROR] {e}"
            s.sendto(response.encode(), addr)
            print(f"[{timestamp()}] [INFO] Sent to {addr}: '{response}'")


if __name__ == "__main__":
    main()
