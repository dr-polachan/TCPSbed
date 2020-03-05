#!/usr/bin/env python

import multiprocessing 
import time
import sys
import os

## load files
execfile("./src/emu_settings.py")

## copying the ns3 program from testbed directory to ns3 directory in emu module
ns3Path = os.path.expanduser(ns3_NS3EmulatorPath)
print ns3Path
os.system ("cp -avr ns3/myEmulation.cc "+ ns3Path+"scratch/myEmulation.cc")

## running the ns3 program from the ns3 directory in emu module
os.chdir(ns3Path)
str_ns3 = "scratch/myEmulation"

os.system ('sudo ./waf --run '+'"scratch/myEmulation '+

"--varDeviceDataRate="+ns3_EmulatedLinkBandwidth+
" --varChannelDelay="+ns3_EmulatedLinkDelay+
" --varErrorModel="+ns3_PacketErrorModel+
" --varErrorRate="+ns3_PacketErrorRate_percent+
" --varIface0="+PC_2_iface_0_label+
" --varIface1="+PC_2_iface_1_label+
" --varSimulatedTrafficDirection="+ns3_SimulatedTrafficDirection+
" --varSimulatedTrafficMode="+ns3_SimulatedTrafficMode+
" --varSimulatedTrafficType="+ns3_SimulatedTrafficType+
" --varSimulatedTraffic_Rate="+ns3_SimulatedTraffic_Rate+
" --varSimulatedTraffic_PacketSize="+ns3_SimulatedTraffic_PacketSize+
" --varEdgeLinkType="+ns3_EdgeLinkType+
" --varWifiAPtoStationDistanceInMeters="+ns3_WifiAPtoStationDistanceInMeters+



'"' )

print "DONE"



