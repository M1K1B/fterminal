import subprocess
import time

interface = input("Enter the intreface name: ")
print()
print("MAC address need to be in format: ww:ww:ww:ww:ww:ww")
new_mac = input("Enter new mac address: ")

print("Configuring" + new_mac + " address...")
time.sleep(5)
print()
print("Changing" + interface + " to" + new_mac)

subprocess.call("ifconfig" + interface + " down", shell=True)
subprocess.call("ifconfig" + interface + " hw ether" + new_mac, shell=True)
subprocess.call("ifconfig" + interface + " up", shell=True)
