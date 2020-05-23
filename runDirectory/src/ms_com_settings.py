import os

execfile("./src/global_settings.py")

### settign ip address for the interfaces for emulation mode
if(testbed_config_mode == "emulation-mode"):
	# setting ip address for the interfaces for emulation mode		
	os.system("sudo ifconfig "+ PC_1_iface_0_label +" 10.1.1.2 netmask 255.255.255.0")

	# settign ip address and routing table information for the emulation mode
	os.system("sudo route add -net 10.1.2.0 netmask 255.255.255.0 gw 10.1.1.1")
	os.system("sudo route add -net 10.1.3.0 netmask 255.255.255.0 gw 10.1.1.1")
	os.system("sudo route add -net 10.1.4.0 netmask 255.255.255.0 gw 10.1.1.1")






