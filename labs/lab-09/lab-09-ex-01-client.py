#!/usr/bin/env python3
import socket

HOST = "httpbin.org"
PORT = 80


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5.0)
            sock.connect((HOST, PORT))

            request = (
                "GET /html HTTP/1.1\r\n"
                f"Host: {HOST}\r\n"
                "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A\r\n"
                "Connection: close\r\n"
                "\r\n"
            )
            print("[INFO] Sending request to server...")
            sock.sendall(request.encode())

            response = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk

            parts = response.split(b"\r\n\r\n", 1)
            headers = parts[0]
            body = parts[1] if len(parts) > 1 else b""

            print(f"[INFO] Received headers:\n{headers.decode(errors='ignore')}")

            with open("lab-09-ex-01-page.html", "wb") as f:
                f.write(body)
            print("[INFO] Saved response body to lab-09-ex-01-page.html")

    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
