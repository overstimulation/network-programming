#!/usr/bin/env python3
import socket

HOST = "212.182.24.27"
PORT = 8080


def fetch_range(start, end):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5.0)
        sock.connect((HOST, PORT))

        range_val = f"{start}-{end}" if end is not None else f"{start}-"
        request = (
            "GET /image.jpg HTTP/1.1\r\n"
            f"Host: {HOST}\r\n"
            f"Range: bytes={range_val}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        print(f"[INFO] Sending request with Range: bytes={range_val}")
        sock.sendall(request.encode())

        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk

        parts = response.split(b"\r\n\r\n", 1)
        body = parts[1] if len(parts) > 1 else b""
        return body


def main():
    try:
        part1 = fetch_range(0, 19)
        part2 = fetch_range(20, 39)
        part3 = fetch_range(40, None)

        full_image = part1 + part2 + part3
        with open("lab-09-ex-03-image.jpg", "wb") as f:
            f.write(full_image)

        print("[INFO] Downloaded all 3 parts and saved to lab-09-ex-03-image.jpg")
    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
