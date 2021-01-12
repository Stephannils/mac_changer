#!/usr/bin/env python

import subprocess
import optparse
import re
import sys


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")

    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error(
            "Please specifiy interface. Use --help for more information")
    elif not options.new_mac:
        parser.error(
            "Please specify new MAC address. User --help for more information")

    return options


def change_mac(interface, new_mac):
    old_mac = get_mac(interface)
    print(
        f"Changing MAC address for {interface} from {old_mac} to {new_mac}")

    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(
        ["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])


def check_mac(req, res):
    if req == res:
        print(f"MAC address changed to {req}")
    else:
        print(f"Could not change MAC address. Please try again")


def get_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",
                    str(ifconfig_result))

    if mac:
        return mac.group(0)
    else:
        print("Interface has no MAC address, Please try with a different interface")
        sys.exit()

try:
    options = get_arguments()
    change_mac(options.interface, options.new_mac)
    check_mac(options.new_mac, get_mac(options.interface))
except:
    pass