#!/usr/bin/env python3
import socket
import base64
import time

HOST = "interia.pl"
PORT = 110


def send_recv(sock, msg=None):
    if msg:
        print(f"[INFO] Client sending: {msg.strip()}")
        sock.sendall(msg.encode())
    time.sleep(0.1)
    try:
        response = sock.recv(4096).decode()
        for line in response.strip().split("\r\n"):
            print(f"[INFO] Server says: {line}")
        return response
    except socket.timeout:
        return ""


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2.0)
            sock.connect((HOST, PORT))

            send_recv(sock)
            send_recv(sock, "USER pas2017@interia.pl\r\n")
            send_recv(sock, "PASS P4SInf2017\r\n")
            res = send_recv(sock, "RETR 1\r\n")

            filename = "downloaded_fallback.png"
            if res:
                lines = res.split("\r\n")
                for line in lines:
                    if "filename=" in line:
                        parts = line.split("filename=")
                        if len(parts) > 1:
                            filename = parts[1].strip('"')
                            break

                b64_data = []
                capture = False
                for line in lines:
                    if capture and line and not line.startswith("--"):
                        if line == ".":
                            break
                        b64_data.append(line)
                    if "Content-Transfer-Encoding: base64" in line:
                        capture = True

                if b64_data:
                    decoded = base64.b64decode("".join(b64_data))
                    with open(filename, "wb") as f:
                        f.write(decoded)
                    print(f"[INFO] Downloaded {filename}")

            send_recv(sock, "QUIT\r\n")
    except Exception as e:
        print(f"[ERROR] Client error: {e}")


if __name__ == "__main__":
    main()
