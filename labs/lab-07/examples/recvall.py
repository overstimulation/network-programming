#!/usr/bin/env python

import socket


def recv_all_until(the_socket, End):
    total_data = [];
    data = ''
    while True:
        data = the_socket.recv(8192)
        if End in data:
            total_data.append(data[:data.find(End)])
            break
        total_data.append(data)
        if len(total_data) > 1:
            last_pair = total_data[-2] + total_data[-1]
            if End in last_pair:
                total_data[-2] = last_pair[:last_pair.find(End)]
                total_data.pop()
                break
    return ''.join(total_data)


def recv_all_until_ver2(sockfd, crlf):
    data = ""
    while not data.endswith(crlf):
        data = data + sockfd.recv(1)
    return data


def recv_all_until_ver3(s, crlf):
    data = ""
    while data[-len(crlf):] != crlf:
        data += s.recv(1)
    return data

def get_resp_code(line):
    return str(line[:3])


if __name__ == "__main__":

    HOST = '212.182.24.27'
    PORT = 110
    SERVER = (HOST, PORT)

    email = "pasumcs@infumcs.edu"
    password = "P4SInf2017"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        sock.connect(SERVER)
        reply = recv_all_until(sock, "\r\n")

        code = get_resp_code(reply)
        if code != "+OK":
            print ('Cannot connect to POP3 server: %s' % reply)
            exit(1)
        else:
            print ('Connected to POP3 server: %s' % reply)

    except:
        pass

sock.close()
