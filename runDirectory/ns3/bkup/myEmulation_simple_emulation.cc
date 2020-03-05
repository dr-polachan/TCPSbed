/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2012 University of Washington, 2012 INRIA 
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

// Allow ns-3 to ping a real host somewhere, using emulation mode
//
//   +----------------------+    
//   |          host        |
//   +----------------------+    
//   |    ns-3 simulation   |                                      
//   +----------------------+                  
//   |      ns-3 Node       |                 
//   |  +----------------+  |                 
//   |  |    ns-3 TCP    |  |              
//   |  +----------------+  |              
//   |  |    ns-3 IPv4   |  |                 
//   |  +----------------+  |                 
//   |  |   FdNetDevice  |  |                
//   |--+----------------+--+     
//   |       | eth0 |       |                
//   |       +------+       |    
//   |          |           |
//   +----------|-----------+ 
//              |
//              |         +---------+
//              .---------| GW host |--- (Internet) -----                             
//                        +---------+ 
//
/// To use this example:
//  1) You need to decide on a physical device on your real system, and either
//     overwrite the hard-configured device name below (eth0) or pass this
//     device name in as a command-line argument
//  2) The host device must be set to promiscuous mode
//     (e.g. "sudo ifconfig eth0 promisc")
//  3) Be aware that ns-3 will generate a fake mac address, and that in
//     some enterprise networks, this may be considered bad form to be
//     sending packets out of your device with "unauthorized" mac addresses
//  4) You will need to assign an IP address to the ns-3 simulation node that
//     is consistent with the subnet that is active on the host device's link.
//     That is, you will have to assign an IP address to the ns-3 node as if
//     it were on your real subnet.  Search for "Ipv4Address localIp" and
//     replace the string "1.2.3.4" with a valid IP address.
//  5) You will need to configure a default route in the ns-3 node to tell it
//     how to get off of your subnet. One thing you could do is a
//     'netstat -rn' command and find the IP address of the default gateway
//     on your host.  Search for "Ipv4Address gateway" and replace the string
//     "1.2.3.4" string with the gateway IP address.
/// 6) Give root suid to the raw socket creator binary.
//     If the --enable-sudo option was used to configure ns-3 with waf, then the following
//     step will not be necessary.
//
//     $ sudo chown root.root build/src/fd-net-device/ns3-dev-raw-sock-creator
//     $ sudo chmod 4755 build/src/fd-net-device/ns3-dev-raw-sock-creator
//

#include "ns3/abort.h"
#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/netanim-module.h"
#include "ns3/network-module.h"
#include "ns3/fd-net-device-module.h"
#include "ns3/internet-apps-module.h"
#include "ns3/ipv4-static-routing-helper.h"
#include "ns3/ipv4-list-routing-helper.h"
#include "ns3/applications-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/csma-module.h"


// KPOL run the program with sudo
// Enable promisc mode 
// Change the ethernet interface
// kpol - you need to run few pings to the rel world for real world
// to ping you back

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("PingEmulationExample");

static void PingRtt (std::string context, Time rtt)
{
  NS_LOG_UNCOND ("Received Response with RTT = " << rtt);
}

int main (int argc, char *argv[])
{
  NS_LOG_INFO ("Ping Emulation Example");

  //
  // Since we are using a real piece of hardware we need to use the realtime
  // simulator.   &
  // Since we are going to be talking to real-world machines, we need to enable
  // calculation of checksums in our protocols.
  //

  GlobalValue::Bind ("SimulatorImplementationType", StringValue ("ns3::RealtimeSimulatorImpl"));
  GlobalValue::Bind ("ChecksumEnabled", BooleanValue (true));

  //--------------------------------------------------------------------------------------------
  
  // KPOL - Creating a node
  NodeContainer mynodes;
  mynodes.Create(3);

  // KPOL - Installing tcp/ip stack on the nodes [one stack per node]
  NS_LOG_INFO ("Add Internet Stack");

  InternetStackHelper internetStackHelper;
  internetStackHelper.Install (mynodes);

  // KPOL - defining the channel 
        // emulated channel emu
        EmuFdNetDeviceHelper emu;
        emu.SetDeviceName ("enx000ec6f99e99"); 

        // emulated channel emu2
        EmuFdNetDeviceHelper emu2;
        emu2.SetDeviceName ("enp8s0"); 
                
        // p2p channel
        PointToPointHelper pointToPoint;
        pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("50000Mbps"));
        pointToPoint.SetChannelAttribute ("Delay", StringValue ("15ms"));

  // KPOL - Wiring the channel/link to the nodes [this step creates devices in the node]      
  
        // wiring the p2p channel to the node-0 and node-1
        
        NodeContainer tempNodeContainer; //creating a temperory node container
        tempNodeContainer.Add(mynodes.Get(0));
        tempNodeContainer.Add(mynodes.Get(1));
        NetDeviceContainer devices_p2p = pointToPoint.Install (tempNodeContainer);

        // wiring the p2p channel to the node-1 and node-2
        NodeContainer tempNodeContainer2; //creating a temperory node container
        tempNodeContainer2.Add(mynodes.Get(1));
        tempNodeContainer2.Add(mynodes.Get(2));
        NetDeviceContainer devices_p2p_2 = pointToPoint.Install (tempNodeContainer2);
        
        // wiring the emu channel to the node-0
        NetDeviceContainer devices = emu.Install (mynodes.Get(0));

        // wiring the emu channel to the node-2       
        NetDeviceContainer device_emu2 = emu2.Install (mynodes.Get(2));

  // KPOL - Assigning ip address to every device [this step creates interfaces from devices]
        
         // assigning address to p2p node-0 and node-1
        Ipv4AddressHelper ipv4address2;
        ipv4address2.SetBase ("10.1.2.0", "255.255.255.0"); //args = network,mask
        Ipv4InterfaceContainer interface2 = ipv4address2.Assign(devices_p2p);
        
         // assigning address to p2p node-1 and node-2
        Ipv4AddressHelper ipv4address3;
        ipv4address3.SetBase ("10.1.3.0", "255.255.255.0"); //args = network,mask
        Ipv4InterfaceContainer interface3 = ipv4address3.Assign(devices_p2p_2);        

        // assigning address to emu device of node-0 [usb-ethernet]
        Ipv4AddressHelper ipv4Address;
        ipv4Address.SetBase("10.1.1.0","255.255.255.0", "0.0.0.1"); // args = network,mask,base
        Ipv4InterfaceContainer interface = ipv4Address.Assign(devices);

        // assigning address to emu device of node-2
        Ipv4AddressHelper ipv4Address4;
        ipv4Address4.SetBase("10.1.4.0","255.255.255.0", "0.0.0.1"); // args = network,mask,base
        Ipv4InterfaceContainer interface4 = ipv4Address4.Assign(device_emu2);
        

  //KPOL - enabling routing protocols
  
        //Ipv4GlobalRoutingHelper::PopulateRoutingTables ();   
          Ptr<Ipv4> ipv4A = mynodes.Get(0)->GetObject<Ipv4> ();
          Ptr<Ipv4> ipv4B = mynodes.Get(1)->GetObject<Ipv4> ();
          Ptr<Ipv4> ipv4C = mynodes.Get(2)->GetObject<Ipv4> ();

        Ipv4StaticRoutingHelper ipv4RoutingHelper;
  
        Ptr<Ipv4StaticRouting> staticRoutingA = ipv4RoutingHelper.GetStaticRouting (ipv4A);
        // The ifIndex for this outbound route is 1; the first p2p link added
        staticRoutingA->AddNetworkRouteTo (Ipv4Address ("10.1.1.0"), Ipv4Mask ("255.255.255.0"), 2);
        staticRoutingA->AddNetworkRouteTo (Ipv4Address ("10.1.2.0"), Ipv4Mask ("255.255.255.0"), 1);
        staticRoutingA->AddNetworkRouteTo (Ipv4Address ("10.1.3.0"), Ipv4Mask ("255.255.255.0"), 1);
        staticRoutingA->AddNetworkRouteTo (Ipv4Address ("10.1.4.0"), Ipv4Mask ("255.255.255.0"), 1);


        Ptr<Ipv4StaticRouting> staticRoutingB = ipv4RoutingHelper.GetStaticRouting (ipv4B);
        // The ifIndex for this outbound route is 1; the first p2p link added
        staticRoutingB->AddNetworkRouteTo (Ipv4Address ("10.1.1.0"), Ipv4Mask ("255.255.255.0"), 1);
        staticRoutingB->AddNetworkRouteTo (Ipv4Address ("10.1.2.0"), Ipv4Mask ("255.255.255.0"), 1);
        staticRoutingB->AddNetworkRouteTo (Ipv4Address ("10.1.3.0"), Ipv4Mask ("255.255.255.0"), 2);
        staticRoutingB->AddNetworkRouteTo (Ipv4Address ("10.1.4.0"), Ipv4Mask ("255.255.255.0"), 2);


        Ptr<Ipv4StaticRouting> staticRoutingC = ipv4RoutingHelper.GetStaticRouting (ipv4C);
        // The ifIndex for this outbound route is 1; the first p2p link added
        staticRoutingC->AddNetworkRouteTo (Ipv4Address ("10.1.1.0"), Ipv4Mask ("255.255.255.0"), 1);
        staticRoutingC->AddNetworkRouteTo (Ipv4Address ("10.1.2.0"), Ipv4Mask ("255.255.255.0"), 1);
        staticRoutingC->AddNetworkRouteTo (Ipv4Address ("10.1.3.0"), Ipv4Mask ("255.255.255.0"), 1);
        staticRoutingC->AddNetworkRouteTo (Ipv4Address ("10.1.4.0"), Ipv4Mask ("255.255.255.0"), 2);


  //KPOL - Configuring client ping application
          V4PingHelper pingClient("10.1.1.2"); //argument is the remote ip
          pingClient.SetAttribute("Verbose", BooleanValue (true));

  //KPOL - Installing Client Application
        ApplicationContainer clientApps = pingClient.Install(mynodes.Get(1));
        clientApps.Start(Seconds(1.0));
        clientApps.Stop(Seconds(10.0));
        //clientApps.Stop(Seconds(1.0));
  
  //KPOL - Giving a name to the client ping applicatino
        Names::Add ("app", clientApps.Get(0));

  //KPOL - Hooking a trace to the client applicatino
        Config::Connect ("/Names/app/Rtt", MakeCallback (&PingRtt));


  // KPOL Running the simulation
  NS_LOG_INFO ("Run Emulation.");
  Simulator::Stop (Seconds (11500.0));
  Simulator::Run ();
  Simulator::Destroy ();
  NS_LOG_INFO ("Done.");
}
