import sys
import tkinter as tk
from tkinter import messagebox

import ipUtilities
import windowsUtilities as osUtilities

def onAuto():
    interfaceName = dropdown_var.get()
    if(interfaceName == ''):
        output_label.config(text='No interface selected')
        return

    interfaceIndex = options.index(interfaceName)
    osUtilities.setAuto(interfaceIndex)
    output_label.config(text=f"Address set automatically via DHCP")


def onGo():
    interfaceName = dropdown_var.get()
    if(interfaceName == ''):
        output_label.config(text='No interface selected')
        return

    # Get inputs
    interfaceIndex = options.index(interfaceName)

    enteredIP = ipBox.get().strip()
    cidr = slider.get()
    enteredGateway = gatewayBox.get().strip()
    subnetMask = ipUtilities.cidrToSubnetMask(cidr)

    if enteredGateway == '':
        setGateway = False
    else:
        setGateway = True
    checksResult = ipUtilities.inputChecks(enteredIP, cidr, enteredGateway, setGateway)
    if checksResult == "OK":
        osUtilities.setIP(enteredIP, subnetMask, enteredGateway, setGateway, interfaceIndex)
        gatewayText = "not set" if not setGateway else enteredGateway
        output_label.config(text=f"IP: {enteredIP}, subnet mask: {cidr} ({subnetMask}), default gateway: {gatewayText}")
    else:
        output_label.config(text=checksResult)

if not osUtilities.isAdmin():
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Admin Privileges Required", "Please run this application as an administrator.")
    sys.exit()

root = tk.Tk()
root.title("Change IP")

options = osUtilities.getInterfacesPreviewList()

dropdown_var = tk.StringVar(root)
dropdown = tk.OptionMenu(root, dropdown_var, *options)
dropdown.pack(pady=10)

# IP address
ipBox = tk.Entry(root, width=30)
ipBox.pack(pady=10)

# Subnet mask slider
slider = tk.Scale(root, from_=0, to=32, orient=tk.HORIZONTAL)
slider.set(24)
slider.pack(pady=10)

# Default gateway
gatewayBox = tk.Entry(root, width=30)
gatewayBox.pack(pady=10)

goButton = tk.Button(root, text="Go", command=onGo)
goButton.pack(pady=5)

autoButton = tk.Button(root, text="Auto (DHCP)", command=onAuto)
autoButton.pack(pady=5)

output_label = tk.Label(root, text="")
output_label.pack(pady=10)

root.mainloop()
