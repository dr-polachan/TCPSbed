
execfile("./src/global_settings.py")

### settign ip address for the interfaces for emulation mode
os.system("sudo ifconfig "+ PC_2_iface_0_label +" 10.1.1.5 netmask 255.255.255.128")
os.system("sudo ifconfig "+ PC_2_iface_1_label +" 10.1.200.5 netmask 255.255.255.128")

### setting the interfaces in promisc mode
os.system("sudo ifconfig "+ PC_2_iface_0_label +" promisc")
os.system("sudo ifconfig "+ PC_2_iface_1_label +" promisc")


