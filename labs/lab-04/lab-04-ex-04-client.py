#!/usr/bin/env python3
import socket

HOST = "212.182.24.27"
PORT = 2902


def main():
    num1 = input("Enter first number: ")
    op = input("Enter operator (+, -, *, /): ")
    num2 = input("Enter second number: ")
    message = f"{num1} {op} {num2}"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(5)
            s.sendto(message.encode(), (HOST, PORT))
            data, _ = s.recvfrom(4096)
            print(f"[INFO] Result: {data.decode()}")
    except socket.timeout:
        print(f"[ERROR] No response from {HOST}:{PORT} (timed out).")


if __name__ == "__main__":
    main()
