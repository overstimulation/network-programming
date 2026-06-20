#!/usr/bin/env python3
import socket
import struct

HOST = "212.182.24.27"
PORT = 2910

RAW = bytes.fromhex(
    "ed 74 0b 55 00 24 ef fd 70 72 6f 67 72 61 "
    "6d 6d 69 6e 67 20 69 6e 20 70 79 74 68 6f "
    "6e 20 69 73 20 66 75 6e"
)


def parse_udp(raw):
    src_port = struct.unpack("!H", raw[0:2])[0]
    dst_port = struct.unpack("!H", raw[2:4])[0]
    data = raw[8:].decode()
    return src_port, dst_port, data


def main():
    src_port, dst_port, data = parse_udp(RAW)
    print(f"[INFO] Parsed UDP: src={src_port}, dst={dst_port}, data='{data}'")

    message = f"zad14odp;src;{src_port};dst;{dst_port};data;{data}"
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
