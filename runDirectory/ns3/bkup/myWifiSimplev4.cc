/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
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

#include "ns3/core-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/network-module.h"
#include "ns3/applications-module.h"
#include "ns3/wifi-module.h"
#include "ns3/mobility-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/internet-apps-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("ThirdScriptExample");


static void PingRtt (std::string context, Time rtt)
{
  NS_LOG_UNCOND ("Received Response with RTT = " << rtt);
}

/*
Kurian's Comments:
Argument can be distance.
*/

int
main (int argc, char *argv[])
{
  
// creating network nodes
        // creating wired nodes
        NodeContainer mynodes;
        mynodes.Create(2);
        // creating wifi station nodes
        NodeContainer wifiStaNodes;
        wifiStaNodes.Create (1); //creating 1 station node

// Adding TCP/IP stack to all nodes
        // installing stack on wired nodes
        InternetStackHelper internetStackHelper;
        internetStackHelper.Install (mynodes);
        // installing stack on wifi station nodes
        InternetStackHelper internetStackHelper2;
        internetStackHelper2.Install (wifiStaNodes); //internet stack for other nodes is defined


  // Defining Channels
        // defining p2p channel
        PointToPointHelper pointToPoint;
        pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));
        pointToPoint.SetChannelAttribute ("Delay", StringValue ("1ms"));
        
        // defining wifi channel and its settings
        YansWifiChannelHelper channel;
        channel.SetPropagationDelay ("ns3::ConstantSpeedPropagationDelayModel");
        channel.AddPropagationLoss ("ns3::LogDistancePropagationLossModel");

        YansWifiPhyHelper phy;
        phy.SetErrorRateModel("ns3::NistErrorRateModel");
        phy.SetChannel (channel.Create ());


// Wiring the channel/link to the nodes [this step creates devices in the node]      

        // wiring the p2p channel to the node-0 and node-1
        NodeContainer tempNodeContainer1; //creating a temperory node container
        tempNodeContainer1.Add(mynodes.Get(0));
        tempNodeContainer1.Add(mynodes.Get(1));
        NetDeviceContainer device_p2p = pointToPoint.Install (tempNodeContainer1);

        // linking wifi nodes to wifi channel and defining wifi settings      
        Ssid ssid = Ssid ("ns-3-ssid");
        WifiMacHelper macWifiStation;
        macWifiStation.SetType ("ns3::StaWifiMac", "Ssid", SsidValue (ssid), "ActiveProbing", BooleanValue (false));
        WifiMacHelper macWifiAP;
        macWifiAP.SetType ("ns3::ApWifiMac", "Ssid", SsidValue (ssid));

        WifiHelper wifi;
        wifi.SetStandard (WIFI_PHY_STANDARD_80211n_5GHZ);
        wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager");
                // linking the wifi station nodes to wifi channel 
                NetDeviceContainer device_wifiStations = wifi.Install (phy, macWifiStation, wifiStaNodes);
                // linking the wifi AP to wifi channel
                NodeContainer wifiApNode = mynodes.Get (1);
                NetDeviceContainer device_wifiAP = wifi.Install (phy, macWifiAP, wifiApNode);

                // defining wifi mobility and positioning the AP and station
                // reference: https://www.nsnam.org/doxygen/80211e-txop_8cc_source.html
                MobilityHelper mobility;
                mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");

                Ptr<ListPositionAllocator> positionAlloc = CreateObject<ListPositionAllocator> ();
                positionAlloc->Add (Vector (0.0, 0.0, 0.0)); // setting position for AP
                double distance = 50; //meters                
                positionAlloc->Add (Vector (distance, 0.0, 0.0)); // setting position for station node
                mobility.SetPositionAllocator (positionAlloc);
                mobility.Install (wifiApNode);
                mobility.Install (wifiStaNodes);


 // Assigning ip address to every device [this step creates interfaces from devices]

  Ipv4AddressHelper address;

  //assigning address to p2p devices
  address.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer p2pInterfaces;
  p2pInterfaces = address.Assign (device_p2p);

  //assigning address to wifi devices
  address.SetBase ("10.1.3.0", "255.255.255.0");
  address.Assign (device_wifiStations);
  address.Assign (device_wifiAP);

  ////    Ping Application
                //Configuring client ping application
                V4PingHelper pingClient("10.1.1.2"); //argument is the remote ip to ping
                pingClient.SetAttribute("Verbose", BooleanValue (true));
                //Installing Client Application
                //ApplicationContainer clientApps = pingClient.Install(wifiApNode.Get(0));
                ApplicationContainer clientApps = pingClient.Install(wifiStaNodes.Get(0));
                clientApps.Start(Seconds(1.0));
                clientApps.Stop(Seconds(5.0));         
                //Giving a name to the client ping applicatin
                Names::Add ("app", clientApps.Get(0));
                //Hooking a trace to the client ping application
                Config::Connect ("/Names/app/Rtt", MakeCallback (&PingRtt));  


  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

  Simulator::Stop (Seconds (1000.0));

  Simulator::Run ();
  Simulator::Destroy ();
  return 0;
}
