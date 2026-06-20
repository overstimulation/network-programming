#!/usr/bin/env python3
import socket

HOST = "212.182.24.27"
TCP_PORT = 2913


def main():
    print(f"[INFO] Starting port knocking sequence on {HOST}")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
        udp_sock.settimeout(0.5)

        sequence_found = False
        for port in range(666, 65536, 1000):
            try:
                udp_sock.sendto(b"PING", (HOST, port))
                data, _ = udp_sock.recvfrom(1024)
                if data.decode().strip() == "PONG":
                    print(f"[INFO] Discovered sequence port: {port}")
                    sequence_found = True
            except socket.timeout:
                pass
            except Exception as e:
                print(f"[ERROR] UDP error on port {port}: {e}")

    if not sequence_found:
        print("[INFO] No sequence ports found. Attempting TCP connection anyway.")

    print(f"[INFO] Connecting to hidden TCP port {TCP_PORT}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
            tcp_sock.settimeout(5.0)
            tcp_sock.connect((HOST, TCP_PORT))
            data = tcp_sock.recv(1024)
            print(f"[INFO] Hidden service says: {data.decode().strip()}")
    except Exception as e:
        print(f"[ERROR] Failed to connect to TCP port {TCP_PORT}: {e}")


if __name__ == "__main__":
    main()
