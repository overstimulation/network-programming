#!/usr/bin/env python3
import socket
import sys
import time

HOST = "127.0.0.1"
MESSAGES_COUNT = 10000
MESSAGE = b"TEST_MESSAGE"


def test_tcp(port):
    start_time = time.time()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, port))
            for _ in range(MESSAGES_COUNT):
                s.sendall(MESSAGE)
                _ = s.recv(1024)
    except Exception as e:
        print(f"[ERROR] TCP error: {e}")
        return float("inf")
    end_time = time.time()
    return end_time - start_time


def test_udp(port):
    start_time = time.time()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            for _ in range(MESSAGES_COUNT):
                s.sendto(MESSAGE, (HOST, port))
                _, _ = s.recvfrom(1024)
    except Exception as e:
        print(f"[ERROR] UDP error: {e}")
        return float("inf")
    end_time = time.time()
    return end_time - start_time


def main():
    if len(sys.argv) != 3:
        print(f"[ERROR] Usage: {sys.argv[0]} <tcp_port> <udp_port>")
        sys.exit(1)

    try:
        tcp_port = int(sys.argv[1])
        udp_port = int(sys.argv[2])
    except ValueError:
        print("[ERROR] Ports must be valid integers.")
        sys.exit(1)

    print(f"[INFO] Testing TCP on {HOST}:{tcp_port} with {MESSAGES_COUNT} messages...")
    tcp_time = test_tcp(tcp_port)
    print(f"[INFO] TCP total time: {tcp_time:.4f} seconds")

    print(f"[INFO] Testing UDP on {HOST}:{udp_port} with {MESSAGES_COUNT} messages...")
    udp_time = test_udp(udp_port)
    print(f"[INFO] UDP total time: {udp_time:.4f} seconds")

    faster = "UDP" if udp_time < tcp_time else "TCP"

    print("\n[INFO] --- THEORETICAL ANSWERS ---")
    print(
        f"[INFO] 1. For which socket is the time shorter? -> The time is shorter for {faster}."
    )
    print(
        "[INFO] 2. What is the reason for the shorter time? -> UDP does not impose the overhead of establishing a connection (3-way handshake), verifying packet delivery, flow control, and retransmitting lost fragments. It sends packets immediately, which minimises delays."
    )
    print("[INFO] 3. What are the advantages / disadvantages of both solutions?")
    print(
        "[INFO]    TCP: Advantages include delivery guarantee, correct order, and flow control. Disadvantages are greater overhead and lower speed."
    )
    print(
        "[INFO]    UDP: Advantages include very low latency and no overhead. Disadvantages are lack of delivery guarantee, possible packet reordering, and data loss."
    )


if __name__ == "__main__":
    main()
