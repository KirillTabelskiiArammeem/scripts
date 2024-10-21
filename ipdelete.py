# /usr/bin/python3

import subprocess


process = subprocess.Popen("ifconfig", stdout=subprocess.PIPE, shell=True)
result, _ = process.communicate()

interfaces = result.decode().split("\n\n")

for interface in interfaces:
    if "inet 172" in interface:
        interface = interface.split(":")[0]
        print(interface)
        subprocess.Popen(f"sudo ip link delete {interface}", shell=True)
