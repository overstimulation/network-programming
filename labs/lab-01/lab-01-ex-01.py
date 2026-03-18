#!/usr/bin/env python3
import sys


def main():
    source_file = input("Enter the name of the source text file: ")
    target_file = "lab1zad1.txt"

    try:
        with open(source_file, "r") as src:
            content = src.read()

        with open(target_file, "w") as dst:
            dst.write(content)

        print("[INFO] File copied successfully.")

    except IOError as error:
        print(f"[ERROR] Could not read or write the file: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
