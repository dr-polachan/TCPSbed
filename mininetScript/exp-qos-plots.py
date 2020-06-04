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

    info( '*** Add switches\n')
    s0 = net.addSwitch('s0', cls=LinuxBridge, failMode='standalone')
    s1 = net.addSwitch('s1', cls=LinuxBridge, failMode='standalone')


    info( '*** Add hosts\n')
    hTEM = net.addHost('hTEM', ip='10.0.0.1/8', mac='00:00:00:00:00:01')
    hTES = net.addHost('hTES', ip='10.0.0.2/8', mac='00:00:00:00:00:02')
    hTx1 = net.addHost('hTx1', ip='10.0.0.3/8', mac='00:00:00:00:00:03')
    hRx1 = net.addHost('hRx1', ip='10.0.0.4/8', mac='00:00:00:00:00:04')
    hTx2 = net.addHost('hTx2', ip='10.0.0.5/8', mac='00:00:00:00:00:05')
    hRx2 = net.addHost('hRx2', ip='10.0.0.6/8', mac='00:00:00:00:00:06')

    info( '*** Add links between hosts and switches\n')
    linkConfig_l = {'delay':'0', 'bw' : 100, 'use_htb':'True'}

    net.addLink(hTEM, s0,cls=TCLink , **linkConfig_l)
    net.addLink(hTx1, s0,cls=TCLink , **linkConfig_l)
    net.addLink(hRx2, s0,cls=TCLink , **linkConfig_l)

    net.addLink(hRx1, s1,cls=TCLink , **linkConfig_l)
    net.addLink(hTx2, s1,cls=TCLink , **linkConfig_l)
    net.addLink(hTES, s1,cls=TCLink , **linkConfig_l)

    net.addLink(s0, s1,cls=TCLink , **linkConfig_l)


    info( '*** Starting network\n')
    net.build()

    net.start()

    #net.pingAll()

    return(net)

def myLoadTestbedComponents(net):

    ### generating cross-traffic
    net.get('hTx1').cmd("sudo nohup ./scripts/Tx1 &")
    net.get('hTx2').cmd("sudo nohup ./scripts/Tx2 &")

    print "*** Loading Testbed Components (START) >>>"
    
    net.get('hTEM').cmd("cd  ../runDirectory/; sudo nohup ./scripts/master &")
    net.get('hTEM').cmd("cd  ../runDirectory/; sudo nohup ./scripts/server &") 
    net.get('hTES').cmd("cd  ../runDirectory/; sudo nohup ./scripts/slave &")     
    net.get('hTES').cmd("cd  ../runDirectory/; sudo nohup ./scripts/slave_ei")     

    print "*** Loading Testbed Components (END) <<<"    

    
if __name__ == '__main__':

    os.system("sudo mn -c")
    setLogLevel( 'info' )

    # clean the results folder
    os.system("sudo rm ../runDirectory/results/qos-analysis/*")
    os.system("sudo rm ../runDirectory/results/edge-experiments/*")

    # Simulate Network Topology
    net = myNetwork()

    # Loading Testbed Components
    myLoadTestbedComponents(net)
    
    CLI(net)
    net.stop()
    # Exit Mininet	
    exit()

