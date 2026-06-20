#!/usr/bin/env python3
import socket
import urllib.parse

HOST = "httpbin.org"
PORT = 80


def main():
    try:
        name = input("Enter name: ")
        email = input("Enter email: ")

        data = {"name": name, "email": email}
        body = urllib.parse.urlencode(data)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5.0)
            sock.connect((HOST, PORT))

            request = (
                "POST /post HTTP/1.1\r\n"
                f"Host: {HOST}\r\n"
                "Content-Type: application/x-www-form-urlencoded\r\n"
                f"Content-Length: {len(body)}\r\n"
                "Connection: close\r\n"
                "\r\n"
                f"{body}"
            )
            print("[INFO] Sending POST request to server...")
            sock.sendall(request.encode())

            response = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk

            parts = response.split(b"\r\n\r\n", 1)
            headers = parts[0]
            resp_body = parts[1] if len(parts) > 1 else b""

            print(f"[INFO] Received headers:\n{headers.decode(errors='ignore')}")
            print(f"[INFO] Received body:\n{resp_body.decode(errors='ignore')}")

    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
