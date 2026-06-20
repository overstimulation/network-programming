#!/usr/bin/env python
import socket

def recv_all_until(sockfd, crlf):
    data = ""
    while not data.endswith(crlf):
        data = data + sockfd.recv(1)
    return data

if __name__ == "__main__":
    pass 