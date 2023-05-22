#!/usr/bin/env python3

import argparse
import getpass
import socket
import subprocess
from os import makedirs, path

from Crypto.Cipher import DES

HOME = path.expanduser("~")
LOC_1 = "-".join(
    [item[::-1] for item in ["3a0629ae", "a054", "0e74", "1c59", "4bbbc15c451f"]]
)
LOC_2 = "-".join(
    [item[::-1] for item in ["59e65f42", "160f", "7b84", "1369", "a353a8f3f42b"]]
)


def pad(text):
    text = text.encode()
    while len(text) % 8 != 0:
        text += b" "
    return text.decode()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("otp", nargs="?", default=None)
    parser.add_argument("-s", "--set", default=False, action="store_true")
    return parser.parse_args()


def _get_f(_path):
    return path.join(HOME, f".{_path}", _path)


def _red_f(path):
    with open(_get_f(path), "rb") as f:
        return f.read()


def _is_one_cred_set(_path):
    return path.exists(_get_f(_path)) and _red_f(_path)


def is_credentials_set():
    return _is_one_cred_set(LOC_1) and _is_one_cred_set(LOC_2)


def get_k():
    k = socket.gethostname()
    if len(k) < 8:
        k = pad(k)
    elif len(k) == 8:
        pass
    else:
        k = k[:8]
    return k.encode()


def c(text):
    return DES.new(get_k(), DES.MODE_ECB).encrypt(pad(text).encode())


def d(text):
    return DES.new(get_k(), DES.MODE_ECB).decrypt(text).decode().strip()


def set_c():
    with open(_get_f(LOC_1), "wb") as f:
        f.write(c(input("l: ")))
    with open(_get_f(LOC_2), "wb") as f:
        f.write(c(getpass.getpass("p: ")))


def get_c():
    return d(_red_f(LOC_1)), d(_red_f(LOC_2))


def main():
    args = get_args()
    makedirs(path.join(HOME, f".{LOC_1}"), exist_ok=True)
    makedirs(path.join(HOME, f".{LOC_2}"), exist_ok=True)
    if args.set or not is_credentials_set():
        set_c()
        print("It was set, restart script")
        return
    if not args.otp:
        args.otp = input("otp: ")
    a, b = get_c()

    proc = subprocess.Popen(
        ["sso-auth", "--U", a, "--P", b, "--p", args.otp], stdout=subprocess.PIPE
    )
    print(proc.communicate()[0].decode())


if __name__ == "__main__":
    main()
