#!/usr/bin/env python3
import socket
import os

HOST = "127.0.0.1"
PORT = int(os.environ.get("IMAP_PORT", 1430))


def handle_client(conn, addr):
    print(f"[INFO] Connection from {addr}")
    try:
        conn.sendall(b"* OK IMAP4rev1 Mock Server Ready\r\n")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            lines = data.decode().split("\r\n")
            for line in lines:
                if not line:
                    continue
                print(f"[INFO] Server received: {line}")
                parts = line.split()
                if len(parts) < 2:
                    conn.sendall(b"* BAD Invalid command\r\n")
                    continue
                tag = parts[0]
                cmd = parts[1].upper()

                if cmd == "LOGIN":
                    conn.sendall(f"{tag} OK Logged in\r\n".encode())
                elif cmd == "LOGOUT":
                    conn.sendall(b"* BYE Logging out\r\n")
                    conn.sendall(f"{tag} OK Logout completed\r\n".encode())
                    return
                elif cmd == "SELECT":
                    conn.sendall(b"* 2 EXISTS\r\n")
                    conn.sendall(b"* 1 RECENT\r\n")
                    conn.sendall(b"* OK [UNSEEN 1]\r\n")
                    conn.sendall(f"{tag} OK [READ-WRITE] Select completed\r\n".encode())
                elif cmd == "STATUS":
                    mailbox = parts[2].strip('"')
                    if mailbox.upper() == "INBOX":
                        conn.sendall(b"* STATUS INBOX (MESSAGES 2)\r\n")
                    else:
                        conn.sendall(f"* STATUS {mailbox} (MESSAGES 3)\r\n".encode())
                    conn.sendall(f"{tag} OK Status completed\r\n".encode())
                elif cmd == "LIST":
                    conn.sendall(b'* LIST (\\HasNoChildren) "/" INBOX\r\n')
                    conn.sendall(b'* LIST (\\HasNoChildren) "/" Archive\r\n')
                    conn.sendall(f"{tag} OK List completed\r\n".encode())
                elif cmd == "SEARCH":
                    conn.sendall(b"* SEARCH 1 2\r\n")
                    conn.sendall(f"{tag} OK Search completed\r\n".encode())
                elif cmd == "FETCH":
                    conn.sendall(b"* 1 FETCH (BODY[TEXT] {10}\r\nTest Email\r\n)\r\n")
                    conn.sendall(f"{tag} OK Fetch completed\r\n".encode())
                elif cmd == "STORE":
                    conn.sendall(b"* 1 FETCH (FLAGS (\\Seen))\r\n")
                    conn.sendall(f"{tag} OK Store completed\r\n".encode())
                elif cmd == "EXPUNGE":
                    conn.sendall(b"* 1 EXPUNGE\r\n")
                    conn.sendall(f"{tag} OK Expunge completed\r\n".encode())
                else:
                    conn.sendall(f"{tag} BAD Unknown command\r\n".encode())
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
    finally:
        conn.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"[INFO] Mock IMAP server listening on {HOST}:{PORT}")
        conn, addr = server.accept()
        handle_client(conn, addr)


if __name__ == "__main__":
    main()
