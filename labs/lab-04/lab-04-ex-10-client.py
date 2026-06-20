#!/usr/bin/env python3
import socket
import struct

HOST = "212.182.24.27"
PORT = 2909

RAW = bytes.fromhex(
    "0b 54 89 8b 1f 9a 18 ec bb b1 64 f2 80 18 "
    "00 e3 67 71 00 00 01 01 08 0a 02 c1 a4 ee "
    "00 1a 4c ee 68 65 6c 6c 6f 20 3a 29"
)


def parse_tcp(raw):
    src_port = struct.unpack("!H", raw[0:2])[0]
    dst_port = struct.unpack("!H", raw[2:4])[0]
    header_len = (raw[12] >> 4) * 4
    data = raw[header_len:].decode()
    return src_port, dst_port, data


def main():
    src_port, dst_port, data = parse_tcp(RAW)
    print(f"[INFO] Parsed TCP: src={src_port}, dst={dst_port}, data='{data}'")

    message = f"zad13odp;src;{src_port};dst;{dst_port};data;{data}"
    print(f"[INFO] Sending: '{message}'")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(5)
            s.sendto(message.encode(), (HOST, PORT))
            response, _ = s.recvfrom(1024)
            print(f"[INFO] Server response: {response.decode()}")
    except socket.timeout:
        print(f"[ERROR] No response from {HOST}:{PORT} (timed out).")


if __name__ == "__main__":
    main()
