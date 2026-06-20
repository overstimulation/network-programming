#!/usr/bin/env python3
import socket
import os

HOST = "127.0.0.1"
PORT = int(os.environ.get("POP3_PORT", 1100))


def handle_client(conn, addr):
    print(f"[INFO] Connection from {addr}")
    try:
        conn.sendall(b"+OK POP3 Mock Server Ready\r\n")
        auth = False
        while True:
            data = conn.recv(1024)
            if not data:
                break
            lines = data.decode().split("\r\n")
            for line in lines:
                if not line:
                    continue
                print(f"[INFO] Server received: {line}")
                cmd = line.upper().split()[0]
                if cmd == "USER":
                    conn.sendall(b"+OK User accepted\r\n")
                elif cmd == "PASS":
                    conn.sendall(b"+OK Pass accepted\r\n")
                    auth = True
                elif cmd == "STAT":
                    if auth:
                        conn.sendall(b"+OK 1 500\r\n")
                    else:
                        conn.sendall(b"-ERR Not authenticated\r\n")
                elif cmd == "LIST":
                    if auth:
                        conn.sendall(b"+OK 1 messages\r\n1 500\r\n.\r\n")
                elif cmd == "RETR":
                    if auth:
                        email_data = (
                            "+OK Message follows\r\n"
                            "Subject: Image Test\r\n"
                            "MIME-Version: 1.0\r\n"
                            "Content-Type: multipart/mixed; boundary=sep\r\n"
                            "\r\n"
                            "--sep\r\n"
                            "Content-Type: text/plain; charset=UTF-8\r\n"
                            "\r\n"
                            "Here is an image.\r\n"
                            "--sep\r\n"
                            'Content-Type: image/png; name="test_attachment.png"\r\n'
                            'Content-Disposition: attachment; filename="test_attachment.png"\r\n'
                            "Content-Transfer-Encoding: base64\r\n"
                            "\r\n"
                            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==\r\n"
                            "--sep--\r\n"
                            ".\r\n"
                        )
                        conn.sendall(email_data.encode())
                elif cmd == "DELE":
                    if auth:
                        conn.sendall(b"+OK Message deleted\r\n")
                elif cmd == "QUIT":
                    conn.sendall(b"+OK Bye\r\n")
                    return
                else:
                    conn.sendall(b"-ERR Unknown command\r\n")
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
    finally:
        conn.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"[INFO] Mock POP3 server listening on {HOST}:{PORT}")
        conn, addr = server.accept()
        handle_client(conn, addr)


if __name__ == "__main__":
    main()
