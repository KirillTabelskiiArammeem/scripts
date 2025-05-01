#/usr/bin/python3

import subprocess


process = subprocess.Popen("ifconfig", stdout=subprocess.PIPE, shell=True)
result, _ = process.communicate()

interfaces = result.decode().split("\n\n")

for interface in interfaces:
    if "inet 172" in interface or "192.168.196.19" in interface:
        interface = interface.split(":")[0]
        print(interface)
        try:
            subprocess.Popen(f"sudo ip link delete {interface}", shell=True)
        except:
            pass


# docker network inspect $(docker network ls | awk '$3 == "bridge" { print $1}') | jq -r '.[] | .Name + " " + .IPAM.Config[0].Subnet' -
