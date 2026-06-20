#!/usr/bin/env python3
import socket
import sys

HOST = "127.0.0.1"


def handle_client(conn, addr):
    print(f"[INFO] Connection accepted from {addr}")
    try:
        conn.sendall(b"220 ESMTP My Custom Server\r\n")
        in_data = False
        buffer = ""
        while True:
            data = conn.recv(4096)
            if not data:
                break

            buffer += data.decode()
            while "\r\n" in buffer:
                line, buffer = buffer.split("\r\n", 1)

                if not line and not in_data:
                    continue
                print(f"[INFO] Server received: {line}")

                if in_data:
                    if line == ".":
                        in_data = False
                        conn.sendall(b"250 2.0.0 Ok: queued\r\n")
                    continue

                cmd = line.upper().split()[0] if line.strip() else ""
                if cmd in ("HELO", "EHLO"):
                    conn.sendall(b"250-MyCustomServer\r\n250-AUTH LOGIN\r\n250 Ok\r\n")
                elif cmd == "AUTH":
                    conn.sendall(b"334 VXNlcm5hbWU6\r\n")
                elif line == "cGFzMjAxN0BpbnRlcmlhLnBs":
                    conn.sendall(b"334 UGFzc3dvcmQ6\r\n")
                elif line == "UDRTSW5mMjAxNw==":
                    conn.sendall(b"235 2.7.0 Authentication successful\r\n")
                elif cmd == "MAIL":
                    conn.sendall(b"250 2.1.0 Ok\r\n")
                elif cmd == "RCPT":
                    conn.sendall(b"250 2.1.5 Ok\r\n")
                elif cmd == "DATA":
                    conn.sendall(b"354 End data with <CR><LF>.<CR><LF>\r\n")
                    in_data = True
                elif cmd == "QUIT":
                    conn.sendall(b"221 2.0.0 Bye\r\n")
                    return
                else:
                    if line.strip():
                        conn.sendall(b"500 5.5.2 Error: command not recognized\r\n")
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
    finally:
        conn.close()
        print(f"[INFO] Connection with {addr} closed")


def main():
    if len(sys.argv) != 2:
        print(f"[ERROR] Usage: {sys.argv[0]} <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("[ERROR] Port must be a valid integer.")
        sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, port))
        server.listen(1)
        print(f"[INFO] Custom SMTP server listening on {HOST}:{port}")

        while True:
            conn, addr = server.accept()
            handle_client(conn, addr)


if __name__ == "__main__":
    main()
