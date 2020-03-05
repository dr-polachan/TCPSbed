
# load files
execfile("./src/server_settings.py")

import os

## settign ip address and routing table information for the emulation mode
if(testbed_config_mode == "emulation_mode"):
	## setting ip address for the interfaces for emulation mode		
	os.system("sudo ifconfig "+ PC_3_iface_0_label +" 10.1.4.2 netmask 255.255.255.0")

	## setting up routing information
	os.system("sudo route add -net 10.1.3.0 netmask 255.255.255.0 gw 10.1.4.1")
	os.system("sudo route add -net 10.1.2.0 netmask 255.255.255.0 gw 10.1.4.1")
	os.system("sudo route add -net 10.1.1.0 netmask 255.255.255.0 gw 10.1.4.1")


