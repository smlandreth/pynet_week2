#!/usr/bin/env python

"""
Exercise: write a script that connects to rtr1 and executes the 'show ip 
interface brief' command.
"""

from __future__ import print_function, unicode_literals

import telnetlib
import time
import socket
import sys
import getpass

TELNET_PORT = 23
TELNET_TIMEOUT = 6

# this is copied from kbyers re: python 2 and 3 compatibility.
def write_bytes(out_data):
    if sys.version_info[0] >= 3:
        if isinstance(out_data, type(u'')):
            return out_data.encode('utf-8')
        elif isinstance(out_data, type(b'')):
            return out_data
    else:
        if isinstance(out_data, type(u'')):
            return out_data.encode('utf-8')
        elif isinstance(out_data, type(str(''))):
            return out_data
    msg = "Invalid value for out_data neither unicode nor byte string: {}".format(out_data)
    raise ValueError(msg)

def write_channel(remote_conn, data):
    """Handle the PY2/PY3 differences to write data out to the device."""
    remote_conn.write(write_bytes(data))

def read_channel(remote_conn):
    """Handle the PY2/PY3 differences to write data out to the device."""
    return remote_conn.read_very_eager().decode('utf-8', 'ignore')

def telnet_connect(ip_addr):
    """ Establish telnet connection """
    try:
        return telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
    except socket.timeout:
        sys.exit("Connection timed out")

def login(remote_conn, username, password):
    """ Login to network device """
    output = remote_conn.read_until(b"Username:", TELNET_TIMEOUT).decode('utf-8', 'ignore')
    write_channel(remote_conn, username + '\n')
    output += remote_conn.read_until(b"Password:", TELNET_TIMEOUT).decode('utf-8', 'ignore')
    write_channel(remote_conn, password + '\n')
    return output

def disable_paging(remote_conn, paging_cmd='terminal length 0'):
    """ disable paging of output """
    return send_command(remote_conn, paging_cmd)

def send_command(remote_conn, cmd):
    """ send a command over the telnet channel """
    cmd = cmd.rstrip()
    write_channel(remote_conn, cmd + '\n')
    time.sleep(1)
    return read_channel(remote_conn)

def main():
    """
    write a script that telnets to rtr1 and runs a command
    """
    try:
        ip_addr = raw_input("IP Address: ")
    except NameError:
        ip_addr = input("IP Address: ")
    ip_addr = ip_addr.strip()
    username = 'pyclass'
    password = getpass.getpass()

    remote_conn = telnet_connect(ip_addr)
    output = login(remote_conn, username, password)

    time.sleep(1)
    read_channel(remote_conn)
    disable_paging(remote_conn)

    output =  send_command(remote_conn, 'show ip int brief')


    print("\n\n")
    print(output)
    print("\n\n")


    remote_conn.close()

    #print "\n\n"
    #print output
    #print "\n\n"

    #remote_conn.close()


if __name__ == "__main__":
    main()
    

