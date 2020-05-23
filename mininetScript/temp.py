#!/usr/bin/python
import os
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.nodelib import LinuxBridge
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.link import  Intf
from subprocess import call
import time
import datetime

execfile("./settings")

def mySimulateExternalTraffic(net):

    info( '*** Traffic Simulation ... \n' )

    varPort = 5001
    varBandwidth = trafficBandwidth 
    varTime = "250000"

    arrHosts = ['h0', 'h1', 'h2', 'h5', 'h6', 'h8']

    for i in range(len(arrHosts)):
        for j in range(len(arrHosts)):
            if(arrHosts[i]!=arrHosts[j]):
                net.get(arrHosts[i]).cmd("iperf -s -u -p ",str(varPort)," &")
                net.get(arrHosts[j]).cmd("iperf -c ",net.get(arrHosts[i]).IP()," -u -b ",str(varBandwidth)," -t ",str(varTime)," -p ",str(varPort)," &")
                varPort  = varPort + 1

def myNetwork():

    info( '********* Project 1Task 1  **********************\n' )
    net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0', controller=OVSController, protocol='tcp', port=6633)

    info( '*** Add switches\n')
    s0 = net.addSwitch('s0', cls=OVSKernelSwitch, failMode='standalone')
    

    info( '*** Add hosts\n')
    hTEM = net.addHost('hTEM', ip='10.0.0.1/8')
    hTES = net.addHost('hTES', ip='10.0.0.3/8')
    hServer = net.addHost('hServer', ip='10.0.0.2/8')	
    
    info( '*** Add links between hosts and switches\n')
    linkConfig_HToS = {'delay':'0', 'bw' : 100}

    L9 = net.addLink(hTEM, s0,cls=TCLink , **linkConfig_HToS)
    L10 = net.addLink(hTES, s0,cls=TCLink , **linkConfig_HToS)
    L11 = net.addLink(hServer, s0,cls=TCLink , **linkConfig_HToS)

    

    info( '*** Starting network\n')
    net.build()

    info( '*** Starting controllers\n')
    c0.start()

    info( '*** Starting switches\n')
    net.get('s0').start([c0])
    

    net.start()

    net.pingAll()

    return(net)

def myLoadTestbedComponents(net):

    print "*** Loading Testbed Components (START) >>>"

    net.get('hTEM').cmd("cd  ../runDirectory/; sudo nohup ./scripts/master &")
    net.get('hServer').cmd("cd  ../runDirectory/; sudo nohup ./scripts/server &") 
    net.get('hTES').cmd("cd  ../runDirectory/; sudo nohup ./scripts/slave")    

    print "*** Loading Testbed Components (END) <<<"    

    
if __name__ == '__main__':

    os.system("sudo mn -c")
    setLogLevel( 'info' )

    # clean the results folder
    os.system("sudo rm ../runDirectory/results/qosAnalysis/*")

    # Simulate Network Topology
    net = myNetwork()

    # Simulate Traffic in the Network
    #mySimulateExternalTraffic(net)

    # Loading Testbed Components
    myLoadTestbedComponents(net)
	
    # Exit Mininet	
    exit()

