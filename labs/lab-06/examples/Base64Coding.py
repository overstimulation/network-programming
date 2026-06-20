#!/usr/bin/python

import base64

def base64_to_text(text):
    try:
        return str(base64.b64decode(text))
    except:
        return str(base64.b64decode(text).decode('utf-8'))


def text_to_base64(text):
    try:
        return str(base64.b64encode(bytes(text)))
    except:
        return str(base64.b64encode(text.encode()))


if __name__ == "__main__":
    print (base64_to_text("SGVsbG8gV29ybGQ="))
    print (text_to_base64("Hello World"))
