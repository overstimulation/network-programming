#!/usr/bin/env python3
import socket
import os
from datetime import datetime

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 13))


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen(1)
            print(f"[INFO] Daytime server listening on {HOST}:{PORT}")

            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"[INFO] Accepted connection from {addr}")
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
                    conn.sendall(now.encode("utf-8"))
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped.")
    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
