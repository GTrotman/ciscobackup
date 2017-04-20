#!/usr/bin/env python

import telnetlib
import os
import time
import subprocess
import dbase
from access import *


def ping(ip):
    status, result = subprocess.getstatusoutput("ping -c1 -w2 " + ip)
    if status == 0:
        return True
    else:
        return False


def main():
    building = dbase.sql()
    query = ('select distinct building from Brooklyn')
    result = building.request(query)
    # print (result)
    build = []

    for i in range(len(result)):
        build.append(result[i][0])

    for b in build:
        building = b.strip()
        ip = dbase.sql()
        query = ("select ip from Brooklyn where building = '%s'" % (building))
        result = ip.request(query)
        # print (result)
        host = []

        for i in range(len(result)):
            host.append(result[i][0])

        for host in host:
            host = host.strip()
            response = ping(host)
            if response is False:
                print(host, "Link Down - Switch is unreachable")
                f = open('DownSwitch.txt', 'a+')
                f.write(host + '\n')
                f.close()
            else:
                try:
                    # Initiate telnet connection
                    print('\nConnecting to %s' % host)
                    tn = telnetlib.Telnet(host)
                    tn.read_until(b"Username:")
                    tn.write(username.encode('ascii') + b"\r\n")
                    tn.read_until(b"Password:")
                    tn.write(password.encode('ascii') + b"\r\n")
                    tn.write(b"terminal length 0" + b"\r\n")

                    # Get hostname of device
                    output = tn.read_until(b"#").decode('UTF-8')
                    hostname = output.replace('#', '')
                    hostname = hostname.strip()

                    # Get config of device
                    tn.write(b"sh run | exclude clock-period"+b"\r\n")
                    tn.write(b"exit"+b"\r\n")
                    time.sleep(.5)
                    output = tn.read_until(b"exit").decode('UTF-8')

                    # Copy config to backup folder
                    mytime = time.strftime('%Y-%m-%d')
                    filename = (hostname + "_" + host + "_" + mytime)
                    filepath = os.path.join('configs', building, hostname, filename)
                    if not os.path.exists(os.path.dirname(filepath)):
                        os.makedirs(os.path.dirname(filepath))
                        with open(filepath, "w") as f:
                            f.write(output)
                            print("\nBackup done for " + host + " successfully!!!!")
                    else:
                        with open(filepath, "w") as f:
                            f.write(output)
                            print("\nBackup done for " + host + " successfully!!!!")
                except Exception as e:
                    print(host, "ERROR: ", e)


if __name__ == '__main__':
    main()
