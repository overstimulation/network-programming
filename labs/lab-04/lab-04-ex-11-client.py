#!/usr/bin/env python3
import socket
import struct

HOST = "212.182.24.27"
PORT = 2911

RAW = bytes.fromhex(
    "45 00 00 4e f7 fa 40 00 38 06 9d 33 d4 b6 18 1b "
    "c0 a8 00 02 0b 54 b9 a6 fb f9 3c 57 c1 0a 06 c1 "
    "80 18 00 e3 ce 9c 00 00 01 01 08 0a 03 a6 eb 01 "
    "00 0b f8 e5 6e 65 74 77 6f 72 6b 20 70 72 6f 67 "
    "72 61 6d 6d 69 6e 67 20 69 73 20 66 75 6e"
)


def parse_ip(raw):
    version = raw[0] >> 4
    ihl = (raw[0] & 0x0F) * 4
    protocol = raw[9]
    src_ip = ".".join(str(b) for b in raw[12:16])
    dst_ip = ".".join(str(b) for b in raw[16:20])
    return version, ihl, protocol, src_ip, dst_ip


def parse_tcp(raw):
    src_port = struct.unpack("!H", raw[0:2])[0]
    dst_port = struct.unpack("!H", raw[2:4])[0]
    header_len = (raw[12] >> 4) * 4
    data = raw[header_len:].decode()
    return src_port, dst_port, data


def main():
    version, ihl, protocol, src_ip, dst_ip = parse_ip(RAW)
    print(
        f"[INFO] Parsed IP: version={version}, src={src_ip}, dst={dst_ip}, protocol={protocol}"
    )

    msg_a = f"zad15odpA;ver;{version};srcip;{src_ip};dstip;{dst_ip};type;{protocol}"
    print(f"[INFO] Sending (A): '{msg_a}'")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(5)
            s.sendto(msg_a.encode(), (HOST, PORT))
            response, _ = s.recvfrom(1024)
            result_a = response.decode()
            print(f"[INFO] Server response (A): {result_a}")

            if result_a == "TAK":
                src_port, dst_port, data = parse_tcp(RAW[ihl:])
                print(
                    f"[INFO] Parsed TCP: src={src_port}, dst={dst_port}, data='{data}'"
                )

                msg_b = f"zad15odpB;srcport;{src_port};dstport;{dst_port};data;{data}"
                print(f"[INFO] Sending (B): '{msg_b}'")
                s.sendto(msg_b.encode(), (HOST, PORT))
                response, _ = s.recvfrom(1024)
                print(f"[INFO] Server response (B): {response.decode()}")
    except socket.timeout:
        print(f"[ERROR] No response from {HOST}:{PORT} (timed out).")


if __name__ == "__main__":
    main()
