#!/usr/bin/env python3
import sys


def is_valid_ipv4(ip_str):
    parts = ip_str.split(".")
    if len(parts) != 4:
        return False

    for part in parts:
        if not part.isdigit():
            return False

        value = int(part)
        if value < 0 or value > 255:
            return False

    return True


def main():
    ip_address = input("Enter an IP address to validate: ").strip()

    if is_valid_ipv4(ip_address):
        print(f"[INFO] '{ip_address}' is a valid IPv4 address.")
    else:
        print(f"[ERROR] '{ip_address}' is NOT a valid IPv4 address.")
        sys.exit(1)


if __name__ == "__main__":
    main()
