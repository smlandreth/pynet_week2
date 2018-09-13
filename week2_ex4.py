#!/usr/bin/env python

"""
Exercise 4: create a script that connects to rtr1 ad rtr2 and prints out both
MIB2 sysName and sysDescr.
"""

from __future__ import print_function, unicode_literals
import getpass
import snmp_helper

SYS_DESCR = '1.3.6.1.2.1.1.1.0'
SYS_NAME = '1.3.6.1.2.1.1.5.0'


def main():
    try:
        ip_addr1 = raw_input("rtr1 IP Address: ")
        ip_addr2 = raw_input("rtr2 IP Address: ")
    except NameError:
        ip_addr1 = input("rtr1 IP Address: ")
        ip_addr2 = input("rtr2 IP Address: ")

    community_string = getpass.getpass(prompt="Community String: ")

    rtr1 = (ip_addr1, community_string, 161)
    rtr2 = (ip_addr2, community_string, 161)

    for a_device in (rtr1, rtr2):
        print("\n-----")
        for the_oid in (SYS_NAME, SYS_DESCR):
            snmp_data = snmp_helper.snmp_get_oid(a_device, oid=the_oid)
            output = snmp_helper.snmp_extract(snmp_data)
            print(output)
        print("\n-----")
    print()

if __name__ == "__main__":
    main()

