#!/usr/bin/env python

import socket


def recv_all_until(sockfd, crlf):
    data = b""
    while not data.endswith(crlf):
        data = data + sockfd.recv(1)
    return data


if __name__ == "__main__":

    HOST = '212.182.24.27'
    PORT = 143
    SERVER = (HOST, PORT)

    email = "pasumcs@infumcs.edu"
    password = "P4SInf2017"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(SERVER)
        reply = recv_all_until(sock, "\r\n".encode())

        if not "OK" in str(reply):
            print ('Cannot connect to IMAP server: %s' % reply)
            exit(1)
        else:
            print ('Connected to IMAP server: %s' % reply)

    except socket.error as e :
        print (str(e))

    sock.close()
