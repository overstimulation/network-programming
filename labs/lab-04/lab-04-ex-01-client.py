#!/usr/bin/env python3
import socket

HOST = "ntp.task.gda.pl"
PORT = 13


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((HOST, PORT))
            s.sendall(b"Hello")
            data = s.recv(1024)
            print(f"[INFO] Date and time from {HOST}: {data.decode().strip()}")
    except socket.timeout:
        print(f"[ERROR] Connection to {HOST}:{PORT} timed out.")
    except ConnectionRefusedError:
        print(f"[ERROR] Connection to {HOST}:{PORT} refused.")
    except OSError as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
