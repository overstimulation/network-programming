#!/usr/bin/env python3
import socket
import os
import select

HOST = "127.0.0.1"
PORT = int(os.environ.get("HTTP_PORT", 8080))


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(20)
            print(f"[INFO] Server listening on {HOST}:{PORT}")

            inputs = [server]

            import time

            start = time.time()
            while inputs and (time.time() - start < 3):
                readable, _, _ = select.select(inputs, [], [], 0.5)
                for s in readable:
                    if s is server:
                        conn, addr = s.accept()
                        print(f"[INFO] Accepted connection from {addr}")
                        inputs.append(conn)
                    else:
                        try:
                            data = s.recv(1024)
                            if not data:
                                inputs.remove(s)
                                s.close()
                        except Exception:
                            inputs.remove(s)
                            s.close()

    except Exception as e:
        print(f"[ERROR] Server error: {e}")


if __name__ == "__main__":
    main()
