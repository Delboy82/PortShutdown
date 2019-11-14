#!/usr/bin/env python
from netmiko import Netmiko
from getpass import getpass

import re
IP = raw_input("IP Address/Hostname: ")
user = raw_input("Username: ")

#Device Connection Profile
cisco1 = {
    "host": IP,
    "username": user,
    "password": getpass(),
    "device_type": "cisco_ios",
}

#Connect to device run command and then disconnect
net_connect = Netmiko(**cisco1)
command = "show interface"
command2 = "sh version | i uptime"
cli_input = net_connect.send_command(command)
uptime = net_connect.send_command(command2)
net_connect.disconnect()

InterfaceName = []
UsageName = []
Counter = []

for m1 in re.finditer("(GigabitEthernet\d.\d.\d+|GigabitEthernet\d.\d+).*?buffers swapped out", cli_input, re.DOTALL):
        m2 = re.search("(?P<interface>GigabitEthernet\d.\d.\d+|GigabitEthernet\d.\d+).*(?P<Usage>Last input never, output never, output hang never).*(?P<CounterStatus>counters never)", m1.group(0), re.DOTALL)
        if m2:

            InterfaceName.append(m2.group("interface"))
            UsageName.append(m2.group("Usage"))
            Counter.append(m2.group("CounterStatus"))
print uptime
for x in range(len(InterfaceName)):

    print (InterfaceName[x], UsageName[x], Counter[x])
