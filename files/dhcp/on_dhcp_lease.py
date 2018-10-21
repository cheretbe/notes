#!/usr/bin/python3

import os
import argparse
import time
import urllib.request
import email.mime.text
import socket
import getpass
import subprocess

def lookup_mac_vendor(mac_address):
    result = ""
    if mac_address:
        for i in range(3):
            vendor = None
            try:
                # Only first 3 octets are needed for manufacturer identification
                # The rest is ommited for privacy reasons
                response = urllib.request.urlopen("https://api.macvendors.com/" + mac_address[:8])
                vendor = response.read().decode(response.info().get_param('charset') or 'utf-8')
            except:
                time.sleep(1)
            if vendor:
                result = vendor
                break
    return(result)

def send_mail(vendor):
    msg = email.mime.text.MIMEText(
        "IP: {ip}\n"
        "Static: {is_static}\n"
        "MAC: {mac}\n"
        "Vendor: {vendor}\n"
        "Host: {host}\n"
        "Static host name: {static}".format(
            ip=options.ip,
            is_static="yes" if options.is_static == "1" else "no",
            mac=options.mac,
            vendor=vendor,
            host=options.host_name,
            static=options.static_host_name
        )
    )
    msg['From'] = getpass.getuser() + "@" + socket.gethostname()
    msg['To'] = options.mail_to
    msg['Subject'] = "New DHCP lease for {} on {}".format(options.host_name, socket.gethostname())
    proc = subprocess.Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=subprocess.PIPE)
    proc.communicate(bytes(msg.as_string(), "UTF-8"))

def forked_main():
    vendor = lookup_mac_vendor(options.mac)
    mac_is_known = False
    if options.mac:
        if os.path.isfile(options.known_macs_file):
            with open(options.known_macs_file) as f:
                for line in f:
                    if line.rstrip().upper() == options.mac.upper():
                        mac_is_known = True
    if not mac_is_known:
        send_mail(vendor)
        if options.mac:
            with open(options.known_macs_file, "a") as f:
                f.write(options.mac + "\n")

parser = argparse.ArgumentParser(description="New DHCP lease event handler")
parser.add_argument("known_macs_file", help="Known MAC-address list file")
parser.add_argument("ip", nargs="?", default="", help="IP address")
parser.add_argument("mac", nargs="?", default="", help="MAC address")
parser.add_argument("host_name", nargs="?", default="", help="Name of the client")
parser.add_argument("static_host_name", nargs="?", default="", help="Matched static host name")
parser.add_argument("is_static", nargs="?", default="", help="IP is static (0 or 1)")
parser.add_argument('-n', '--no-fork', dest='no_fork', action='store_true',
    default=False, help='Do not fork a child process')
parser.add_argument('-m', '--mail-to', dest='mail_to', default="root",
    help='Mail message recipient (default: root)', metavar="mail")

options = parser.parse_args()

if options.no_fork:
    print("--no-fork option is specified. Running in foreground")
    print("IP: {}".format(options.ip))
    print("MAC: {}".format(options.mac))
    print("Mail to: {}".format(options.mail_to))
    forked_main()
elif os.fork() == 0:
    forked_main()
    os._exit(0)
