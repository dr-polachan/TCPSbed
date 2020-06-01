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

def myNetwork():

    info( '********* Project 1Task 1  **********************\n' )
    net = Mininet( topo=None, build=False, ipBase='10.0.0.0/8')


    info( '*** Adding controller\n' )
    c0=net.addController(name='c0', controller=OVSController, protocol='tcp', port=6633)

    info( '*** Add switches\n')
    s0 = net.addSwitch('s0', cls=OVSKernelSwitch, failMode='standalone')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add hosts\n')
    hTEM = net.addHost('hTEM', ip='10.0.0.1/8')
    hServer = net.addHost('hServer', ip='10.0.0.2/8')   
    hSSEI = net.addHost('hSSEI', ip='10.0.0.3/8')
    hTES = net.addHost('hTES', ip='10.0.0.4/8')

    
    info( '*** Add links between hosts and switches\n')
    linkConfig_HToS = {'delay':'0', 'bw' : 100, 'use_htb':'True'}
    linkConfig_SToS = {'delay':'0', 'bw' : 100, 'use_htb':'True'}
    linkConfig_lastmile = {'delay':'0', 'bw' : 100, 'loss' : 0, 'use_htb':'True' }



    l0=net.addLink(hTEM, s0,cls=TCLink , **linkConfig_HToS)
    l1=net.addLink(s0, s1,cls=TCLink , **linkConfig_SToS)
    l2=net.addLink(hServer, s1,cls=TCLink , **linkConfig_HToS)
    l3=net.addLink(s1, s2,cls=TCLink , **linkConfig_SToS)
    l4=net.addLink(hSSEI, s2,cls=TCLink , **linkConfig_HToS)
    l5=net.addLink(s2, s3,cls=TCLink , **linkConfig_lastmile)
    l6=net.addLink(hTES, s3,cls=TCLink , **linkConfig_HToS)
   

    info( '*** Starting network\n')
    net.build()

    info( '*** Starting switches\n')
    net.get('s0').start([c0])
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])

    

    net.start()

    #net.pingAll()

    return(net)

def myLoadTestbedComponents(net):

    print "*** Loading Testbed Components (START) >>>"

    net.get('hTEM').cmd("cd  ../runDirectory/; sudo nohup ./scripts/master &")
    net.get('hServer').cmd("cd  ../runDirectory/; sudo nohup ./scripts/server &") 
    net.get('hSSEI').cmd("cd  ../runDirectory/; sudo nohup ./scripts/slave_ei &")    
    net.get('hTES').cmd("cd  ../runDirectory/; sudo nohup ./scripts/slave")    

    print "*** Loading Testbed Components (END) <<<"    

    
if __name__ == '__main__':

    os.system("sudo mn -c")
    setLogLevel( 'info' )

    # clean the results folder
    os.system("sudo rm ../runDirectory/results/edge-experiments/*")

    # Simulate Network Topology
    net = myNetwork()

    # Simulate Traffic in the Network
    #mySimulateExternalTraffic(net)

    # Loading Testbed Components
    myLoadTestbedComponents(net)
	
    # Exit Mininet	
    exit()

