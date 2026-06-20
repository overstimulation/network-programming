#!/usr/bin/env python3
import socket

HOST = "212.182.24.27"
PORT = 8080


def fetch_file(modified_since):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5.0)
        sock.connect((HOST, PORT))

        request = (
            "GET /image.jpg HTTP/1.1\r\n"
            f"Host: {HOST}\r\n"
            f"If-Modified-Since: {modified_since}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        print(f"[INFO] Sending request with If-Modified-Since: {modified_since}")
        sock.sendall(request.encode())

        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk

        parts = response.split(b"\r\n\r\n", 1)
        headers = parts[0].decode(errors="ignore")
        body = parts[1] if len(parts) > 1 else b""

        print(f"[INFO] Response headers:\n{headers}")

        if "304 Not Modified" in headers:
            print("[INFO] Server returned 304. File has not changed.")
            return None
        return body


def main():
    try:
        last_check = "Wed, 21 Oct 2015 07:28:00 GMT"
        body = fetch_file(last_check)

        if body:
            with open("lab-09-ex-06-image.jpg", "wb") as f:
                f.write(body)
            print("[INFO] Downloaded file and saved to lab-09-ex-06-image.jpg")

    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
