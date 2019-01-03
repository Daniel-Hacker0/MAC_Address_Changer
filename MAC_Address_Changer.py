#Disclaimer:  
# This code is made for education and ethical testing purposes only.  
# Usage of this tool for attacking targets without permission is illegal.
# I assume no liability and am not responsible for any misuse or damage caused by this code.


import subprocess
import optparse
import re

def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-i", "--interface_name", dest="interface_name", help="Input the interface you want to change")
	parser.add_option("-m", "--MAC", dest="updated_mac", help="New MAC address")
	(options, arguments) = parser.parse_args()
	if not options.interface_name:
		parser.error("[-] Specify an interface name, use --help for more information.")
	elif not options.updated_mac:
		parser.error("[-] Specify a new MAC address, use --help for more information.")
	return options

def change_mac_address(interface_name,updated_mac):
	print("[+] Changing MAC address for " + interface_name + " to " + updated_mac)
	subprocess.call(["ifconfig", interface_name, "down"])
	subprocess.call(["ifconfig", interface_name, "hw", "ether", updated_mac])
	subprocess.call(["ifconfig", interface_name, "up"])

def get_initial_mac_address(interface_name):
	ifconfig_output = subprocess.check_output(["ifconfig", interface_name])
	mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output)
	if mac_address_search_result:
		return mac_address_search_result.group(0)
	else:
		print("[-] Could not find MAC address.")

options = get_arguments()
initial_mac = get_initial_mac_address(options.interface_name)
print("Initial MAC Address = " + str(initial_mac))
change_mac_address(options.interface_name, options.updated_mac)

initial_mac = get_initial_mac_address(options.interface_name)
if initial_mac == options.updated_mac:
	print("[+] MAC address was successfully changed to " + str(initial_mac))
else:
	print("[-] MAC address did not get changed.")