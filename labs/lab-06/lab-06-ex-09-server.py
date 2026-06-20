#!/usr/bin/env python3
import socket
import os

HOST = "127.0.0.1"
PORT = int(os.environ.get("SMTP_PORT", 587))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"[INFO] Mock SMTP server listening on {HOST}:{PORT}")

        conn, addr = server.accept()
        print(f"[INFO] Connection from {addr}")
        try:
            conn.sendall(b"220 ESMTP Mock Server\r\n")
            buffer = ""
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                buffer += data.decode()
                while "\r\n" in buffer:
                    line, buffer = buffer.split("\r\n", 1)
                    if not line:
                        continue
                    print(f"[INFO] Server received: {line}")
                    cmd = line.upper().split()[0]
                    if cmd in ("HELO", "EHLO"):
                        conn.sendall(b"250-MockServer\r\n250-AUTH LOGIN\r\n250 Ok\r\n")
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
                    elif line == ".":
                        conn.sendall(b"250 Ok: queued as 12345\r\n")
                    elif cmd == "QUIT":
                        conn.sendall(b"221 2.0.0 Bye\r\n")
                        break
        except Exception as e:
            print(f"[ERROR] Server error: {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    main()
