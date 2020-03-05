/*

Author: Kurian Polachan, IISc Bangalore
Date: June 10, 2018

- run this code with emu.py of the testbed, sudo emu.py
- for develpment purpose set EMULATIONMODE to 0 else set to 1

*/

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
#include "ns3/wifi-module.h"
#include "ns3/mobility-module.h"


#define EMULATORMODE 1 //this is for debugging/development purpose

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("PingEmulationExample");

static void PingRtt (std::string context, Time rtt)
{
  NS_LOG_UNCOND ("Received Response with RTT = " << rtt);
}

int main (int argc, char *argv[])
{

  // Set default values to command line arguments

        std::string varDeviceDataRate = "5Mbps";
        std::string varChannelDelay = "15ms";
        std::string varErrorModel = "RateErrorModel";
        std::string varIface0 = "enx000ec6f99e99";
        std::string varIface1 = "enp8s0";
        double varErrorRate = 0; //error rate in percentage
        
        std::string varSimulatedTrafficDirection ="fwd";
        std::string varSimulatedTrafficMode = "udp";
        std::string varSimulatedTrafficType = "const"; //"const" or not       
        std::string varSimulatedTraffic_Rate = "50kb/s";
        uint32_t varSimulatedTraffic_PacketSize = 1500;

	std::string varEdgeLinkType = "p2p";
        uint32_t varWifiAPtoStationDistanceInMeters = 50;


  // Reading commandline arguments
        CommandLine cmd;
        cmd.AddValue ("varDeviceDataRate", "Device data rate, example 10Mbps", varDeviceDataRate);
        cmd.AddValue ("varChannelDelay", "Channel delay, example 1ms", varChannelDelay);
        cmd.AddValue ("varErrorModel", "Error model to use. RateErrorModel or BurstErrorModel", varErrorModel);
        cmd.AddValue ("varErrorRate", "Error rate to simulate, example 0.1 implies 10percent", varErrorRate);
        cmd.AddValue ("varIface0", "Network interface linking ms-com", varIface0);
        cmd.AddValue ("varIface1", "Network interface linking ss-com", varIface1);
        cmd.AddValue ("varSimulatedTrafficDirection", "Simulated traffic direction fwd, bwd, fwd/bwd, NaN", varSimulatedTrafficDirection);
        cmd.AddValue ("varSimulatedTrafficMode", "Simulated traffic mode tcp or udp", varSimulatedTrafficMode);
        cmd.AddValue ("varSimulatedTrafficType", "Simulated traffic = const or not, not implies on/off", varSimulatedTrafficType);
        cmd.AddValue ("varSimulatedTraffic_Rate", "Rate of simulated traffic in kb/s", varSimulatedTraffic_Rate);
        cmd.AddValue ("varSimulatedTraffic_PacketSize", "Packet size of simulated traffic", varSimulatedTraffic_PacketSize);
        cmd.AddValue ("varEdgeLinkType", "Edge link type", varEdgeLinkType);
        cmd.AddValue ("varWifiAPtoStationDistanceInMeters", "Wifi AP to station distance", varWifiAPtoStationDistanceInMeters);
        
        cmd.Parse (argc,argv);
        
  // Commands for enabling emulation
        #if EMULATORMODE == 1

        GlobalValue::Bind ("SimulatorImplementationType", StringValue ("ns3::RealtimeSimulatorImpl"));
        GlobalValue::Bind ("ChecksumEnabled", BooleanValue (true));
        #endif
  
  // Creating nodes
  NodeContainer mynodes;
  mynodes.Create(10);

  // Adding TCP/IP stack to all nodes
  InternetStackHelper internetStackHelper;
  internetStackHelper.Install (mynodes);

  // Defining the channel 
        
        #if EMULATORMODE == 1
       
        // emulated channel emu
        EmuFdNetDeviceHelper emu;
        emu.SetDeviceName (varIface0); 

        // emulated channel emu2
        EmuFdNetDeviceHelper emu2;
        emu2.SetDeviceName (varIface1); 
        
        #endif
                
        // p2p channel-1
        PointToPointHelper pointToPoint;
        pointToPoint.SetDeviceAttribute ("DataRate", StringValue (varDeviceDataRate));
        pointToPoint.SetChannelAttribute ("Delay", StringValue (varChannelDelay));

        // p2p channel-2 [dummy]
        PointToPointHelper pointToPointDummy;
        pointToPointDummy.SetDeviceAttribute ("DataRate", StringValue ("1000000Mbps"));
        pointToPointDummy.SetChannelAttribute ("Delay", StringValue ("0ms"));

	// wifi channel 
        YansWifiChannelHelper channel;
        channel.SetPropagationDelay ("ns3::ConstantSpeedPropagationDelayModel");
        channel.AddPropagationLoss ("ns3::LogDistancePropagationLossModel");

        YansWifiPhyHelper phy;
        phy.SetErrorRateModel("ns3::NistErrorRateModel");
        phy.SetChannel (channel.Create ());

  // Wiring the channel/link to the nodes [this step creates devices in the node]      
  
        // wiring the p2p channel to the node-0 and node-1        
        NodeContainer tempNodeContainer2; //creating a temperory node container
        tempNodeContainer2.Add(mynodes.Get(0));
        tempNodeContainer2.Add(mynodes.Get(1));
        NetDeviceContainer devices_p2p_2 = pointToPointDummy.Install (tempNodeContainer2);

        // wiring the p2p channel to the node-1 and node-2
        NodeContainer tempNodeContainer3; //creating a temperory node container
        tempNodeContainer3.Add(mynodes.Get(1));
        tempNodeContainer3.Add(mynodes.Get(2));
        NetDeviceContainer devices_p2p_3 = pointToPoint.Install (tempNodeContainer3);

	//// Edge Link >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  		
	NetDeviceContainer devices_p2p_4;

        NetDeviceContainer device_wifiAP;
        NetDeviceContainer device_wifiStations;
	
	if ( varEdgeLinkType.compare("wifi") == 0)
	{		
			
		Ssid ssid = Ssid ("ns-3-ssid");
		WifiMacHelper macWifiStation;
		macWifiStation.SetType ("ns3::StaWifiMac", "Ssid", SsidValue (ssid), "ActiveProbing", BooleanValue (false));
		WifiMacHelper macWifiAP;
		macWifiAP.SetType ("ns3::ApWifiMac", "Ssid", SsidValue (ssid));

		WifiHelper wifi;
		wifi.SetStandard (WIFI_PHY_STANDARD_80211n_5GHZ);
		wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager");

                NodeContainer wifiApNode = mynodes.Get (2);  // linking the wifi AP to wifi channel
                NodeContainer wifiStaNodes = mynodes.Get (3);  // linking the wifi station to wifi channel

                // defining wifi mobility and positioning the AP and station
                // reference: https://www.nsnam.org/doxygen/80211e-txop_8cc_source.html
                MobilityHelper mobility;
                mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
                Ptr<ListPositionAllocator> positionAlloc = CreateObject<ListPositionAllocator> ();
                positionAlloc->Add (Vector (0.0, 0.0, 0.0)); // setting position for AP
                positionAlloc->Add (Vector (varWifiAPtoStationDistanceInMeters, 0.0, 0.0)); // setting position for station node
                mobility.SetPositionAllocator (positionAlloc);
                mobility.Install (wifiApNode);
                mobility.Install (wifiStaNodes);

                // linking the wifi station nodes to wifi channel 
                device_wifiAP = wifi.Install (phy, macWifiAP, wifiApNode);
                device_wifiStations = wifi.Install (phy, macWifiStation, wifiStaNodes);

		devices_p2p_4 = device_wifiAP;
		devices_p2p_4.Add(device_wifiStations);
		

		//NodeContainer tempNodeContainer4; //creating a temperory node container
		//tempNodeContainer4.Add(mynodes.Get(2));
		//tempNodeContainer4.Add(mynodes.Get(3));
		//devices_p2p_4 = pointToPoint.Install (tempNodeContainer4);

	}

	// wiring the p2p channel to the node-2 and node-3
	else 
	{	
		NodeContainer tempNodeContainer4; //creating a temperory node container
		tempNodeContainer4.Add(mynodes.Get(2));
		tempNodeContainer4.Add(mynodes.Get(3));
		devices_p2p_4 = pointToPointDummy.Install (tempNodeContainer4);
	}



	// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        NodeContainer tempNodeContainer5; //creating a temperory node container
        tempNodeContainer5.Add(mynodes.Get(4));
        tempNodeContainer5.Add(mynodes.Get(1));
        NetDeviceContainer devices_p2p_5 = pointToPointDummy.Install (tempNodeContainer5);

        NodeContainer tempNodeContainer6; //creating a temperory node container
        tempNodeContainer6.Add(mynodes.Get(2));
        tempNodeContainer6.Add(mynodes.Get(5));
        NetDeviceContainer devices_p2p_6 = pointToPointDummy.Install (tempNodeContainer6);
        

        NodeContainer tempNodeContainer7; //creating a temperory node container
        tempNodeContainer7.Add(mynodes.Get(6));
        tempNodeContainer7.Add(mynodes.Get(1));
        NetDeviceContainer devices_p2p_7 = pointToPointDummy.Install (tempNodeContainer7);

        NodeContainer tempNodeContainer8; //creating a temperory node container
        tempNodeContainer8.Add(mynodes.Get(2));
        tempNodeContainer8.Add(mynodes.Get(7));
        NetDeviceContainer devices_p2p_8 = pointToPointDummy.Install (tempNodeContainer8);

	NodeContainer tempNodeContainerA; //creating a temperory node container
        tempNodeContainerA.Add(mynodes.Get(0));
        tempNodeContainerA.Add(mynodes.Get(8));
        NetDeviceContainer devices_dummyMasterSide = pointToPoint.Install (tempNodeContainerA);

	NodeContainer tempNodeContainerB; //creating a temperory node container
        tempNodeContainerB.Add(mynodes.Get(3));
        tempNodeContainerB.Add(mynodes.Get(9));
        NetDeviceContainer devices_dummySlaveSide = pointToPoint.Install (tempNodeContainerB);

        #if EMULATORMODE == 1

        // wiring the emu channel to the node-0 (ms com side)
        NetDeviceContainer devices = emu.Install (mynodes.Get(0));

        // wiring the emu channel to the node-2       
        NetDeviceContainer device_emu2 = emu2.Install (mynodes.Get(3));

        #endif

  // Assigning ip address to every device [this step creates interfaces from devices]
        
         // assigning address to p2p node-0 and node-1
        Ipv4AddressHelper ipv4address2;
        ipv4address2.SetBase ("10.1.2.0", "255.255.255.0"); //args = network,mask
        Ipv4InterfaceContainer interface2 = ipv4address2.Assign(devices_p2p_2); 
        //Note: kpol- interface2.Get(0).second correspond to interface details of node-0
        //Note: kpol- interface2.Get(1).second correspond to interface details of node-1
        
         // assigning address to p2p node-1 and node-2
        Ipv4AddressHelper ipv4address3;
        ipv4address3.SetBase ("10.1.3.0", "255.255.255.0"); //args = network,mask
        Ipv4InterfaceContainer interface3 = ipv4address3.Assign(devices_p2p_3);        
        

	//// Edge Link >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
	
	// assigning address to p2p node-2 and node-3
	Ipv4AddressHelper ipv4address4;
	ipv4address4.SetBase ("10.1.4.0", "255.255.255.0"); //args = network,mask
	Ipv4InterfaceContainer interface4 = ipv4address4.Assign(devices_p2p_4); 

	// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        // assigning address to p2p node-4 and node-1
        Ipv4AddressHelper ipv4address5;
        ipv4address5.SetBase ("10.1.5.0", "255.255.255.0"); //args = network,mask
        Ipv4InterfaceContainer interface5 = ipv4address5.Assign(devices_p2p_5);

        // assigning address to p2p node-2 and node-5
        Ipv4AddressHelper ipv4address6;
        ipv4address6.SetBase ("10.1.6.0", "255.255.255.0"); //args = network,mask
        Ipv4InterfaceContainer interface6 = ipv4address6.Assign(devices_p2p_6); 

        // assigning address to p2p node-6 and node-1
        Ipv4AddressHelper ipv4address7;
        ipv4address7.SetBase ("10.1.7.0", "255.255.255.0"); //args = network,mask
        Ipv4InterfaceContainer interface7 = ipv4address7.Assign(devices_p2p_7);

        // assigning address to p2p node-2 and node-7
        Ipv4AddressHelper ipv4address8;
        ipv4address8.SetBase ("10.1.8.0", "255.255.255.0"); //args = network,mask
        Ipv4InterfaceContainer interface8 = ipv4address8.Assign(devices_p2p_8);

	
	// assigning address to p2p node-0 and node-8 (dummyMasterSide) ----
        Ipv4AddressHelper ipv4addressA;
        ipv4addressA.SetBase ("10.1.1.0", "255.255.255.0", "0.0.0.3"); //args = network,mask
        Ipv4InterfaceContainer interfaceA = ipv4addressA.Assign(devices_dummyMasterSide);
	
	// assigning address to p2p node-0 and node-8 (dummyMasterSide)----
        Ipv4AddressHelper ipv4addressB;
        ipv4addressB.SetBase ("10.1.200.0", "255.255.255.0", "0.0.0.3"); //args = network,mask
        Ipv4InterfaceContainer interfaceB = ipv4addressB.Assign(devices_dummySlaveSide);
	
	

        #if EMULATORMODE == 1
        
        // assigning address to emu device of node-0 (ms com side)
        Ipv4AddressHelper ipv4Address;
        ipv4Address.SetBase("10.1.1.0","255.255.255.128", "0.0.0.1"); // args = network,mask,base
        Ipv4InterfaceContainer interfaceEMU1 = ipv4Address.Assign(devices);

        // assigning address to emu device of node-2 (ss com side)
        Ipv4AddressHelper ipv4Address4;
        ipv4Address4.SetBase("10.1.200.0","255.255.255.128", "0.0.0.1"); // args = network,mask,base
        Ipv4InterfaceContainer interfaceEMU2 = ipv4Address4.Assign(device_emu2);
        
        #endif

  //ns3 static routing
  
        Ipv4GlobalRoutingHelper::PopulateRoutingTables ();   

	/*
          Ptr<Ipv4> ipv40 = mynodes.Get(0)->GetObject<Ipv4> (); //kpol check if we can use interface2.Get(0).first method ?
          Ptr<Ipv4> ipv41 = mynodes.Get(1)->GetObject<Ipv4> ();
          Ptr<Ipv4> ipv42 = mynodes.Get(2)->GetObject<Ipv4> ();
          Ptr<Ipv4> ipv43 = mynodes.Get(3)->GetObject<Ipv4> ();
          Ptr<Ipv4> ipv44 = mynodes.Get(4)->GetObject<Ipv4> ();
          Ptr<Ipv4> ipv45 = mynodes.Get(5)->GetObject<Ipv4> ();
          Ptr<Ipv4> ipv46 = mynodes.Get(6)->GetObject<Ipv4> ();
          Ptr<Ipv4> ipv47 = mynodes.Get(7)->GetObject<Ipv4> ();

        Ipv4StaticRoutingHelper ipv4RoutingHelper;
  
        Ptr<Ipv4StaticRouting> staticRouting0 = ipv4RoutingHelper.GetStaticRouting (ipv40);
        // The ifIndex for this outbound route is 1; the first p2p link added
        staticRouting0->AddNetworkRouteTo (Ipv4Address ("10.1.1.0"), Ipv4Mask ("255.255.255.0"), 2);
        staticRouting0->AddNetworkRouteTo (Ipv4Address ("10.1.2.0"), Ipv4Mask ("255.255.255.0"), 1); //interface2.Get(0).second); // interface2.Get(0).second);
        staticRouting0->AddNetworkRouteTo (Ipv4Address ("10.1.3.0"), Ipv4Mask ("255.255.255.0"), 1); //interface2.Get(0).second); //interface2.Get(0).second);
        staticRouting0->AddNetworkRouteTo (Ipv4Address ("10.1.4.0"), Ipv4Mask ("255.255.255.0"), 1); //interface2.Get(0).second);
        staticRouting0->AddNetworkRouteTo (Ipv4Address ("10.1.200.0"), Ipv4Mask ("255.255.255.0"), 1); //interface2.Get(0).second);
        staticRouting0->AddNetworkRouteTo (Ipv4Address ("10.1.5.0"), Ipv4Mask ("255.255.255.0"), 1); //interface2.Get(0).second);
        staticRouting0->AddNetworkRouteTo (Ipv4Address ("10.1.6.0"), Ipv4Mask ("255.255.255.0"), 1); //interface2.Get(0).second);


        Ptr<Ipv4StaticRouting> staticRouting1 = ipv4RoutingHelper.GetStaticRouting (ipv41);
        // The ifIndex for this outbound route is 1; the first p2p link added
        staticRouting1->AddNetworkRouteTo (Ipv4Address ("10.1.1.0"), Ipv4Mask ("255.255.255.0"), 1);
        staticRouting1->AddNetworkRouteTo (Ipv4Address ("10.1.2.0"), Ipv4Mask ("255.255.255.0"), 1);
        staticRouting1->AddNetworkRouteTo (Ipv4Address ("10.1.3.0"), Ipv4Mask ("255.255.255.0"), 2);
        staticRouting1->AddNetworkRouteTo (Ipv4Address ("10.1.4.0"), Ipv4Mask ("255.255.255.0"), 2);
        staticRouting1->AddNetworkRouteTo (Ipv4Address ("10.1.200.0"), Ipv4Mask ("255.255.255.0"), 2);
        staticRouting1->AddNetworkRouteTo (Ipv4Address ("10.1.6.0"), Ipv4Mask ("255.255.255.0"), 2); //interface6.Get(1).second);
        staticRouting1->AddNetworkRouteTo (Ipv4Address ("10.1.5.0"), Ipv4Mask ("255.255.255.0"), 3); //interface6.Get(1).second);
        staticRouting1->AddNetworkRouteTo (Ipv4Address ("10.1.7.0"), Ipv4Mask ("255.255.255.0"), 4); //interface6.Get(1).second);
        staticRouting1->AddNetworkRouteTo (Ipv4Address ("10.1.8.0"), Ipv4Mask ("255.255.255.0"), 2); //interface6.Get(1).second);



        Ptr<Ipv4StaticRouting> staticRouting2 = ipv4RoutingHelper.GetStaticRouting (ipv42);
        // The ifIndex for this outbound route is 1; the first p2p link added
        staticRouting2->AddNetworkRouteTo (Ipv4Address ("10.1.1.0"), Ipv4Mask ("255.255.255.0"), 1); //you can also use 1 or 2
        staticRouting2->AddNetworkRouteTo (Ipv4Address ("10.1.2.0"), Ipv4Mask ("255.255.255.0"), 1);
        staticRouting2->AddNetworkRouteTo (Ipv4Address ("10.1.3.0"), Ipv4Mask ("255.255.255.0"), 1); //interface4.Get(0).second);
        staticRouting2->AddNetworkRouteTo (Ipv4Address ("10.1.4.0"), Ipv4Mask ("255.255.255.0"), 2); //interface4.Get(0).second);
        staticRouting2->AddNetworkRouteTo (Ipv4Address ("10.1.200.0"), Ipv4Mask ("255.255.255.0"), 2); //interface4.Get(0).second);
        staticRouting2->AddNetworkRouteTo (Ipv4Address ("10.1.5.0"), Ipv4Mask ("255.255.255.0"), 1); //interface4.Get(0).second);
        staticRouting2->AddNetworkRouteTo (Ipv4Address ("10.1.6.0"), Ipv4Mask ("255.255.255.0"), 3); //interface4.Get(0).second);
        staticRouting2->AddNetworkRouteTo (Ipv4Address ("10.1.7.0"), Ipv4Mask ("255.255.255.0"), 1); //interface4.Get(0).second);
        staticRouting2->AddNetworkRouteTo (Ipv4Address ("10.1.8.0"), Ipv4Mask ("255.255.255.0"), 4); //interface4.Get(0).second);

        Ptr<Ipv4StaticRouting> staticRouting3 = ipv4RoutingHelper.GetStaticRouting (ipv43);
        // The ifIndex for this outbound route is 1; the first p2p link added
        staticRouting3->AddNetworkRouteTo (Ipv4Address ("10.1.1.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting3->AddNetworkRouteTo (Ipv4Address ("10.1.2.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting3->AddNetworkRouteTo (Ipv4Address ("10.1.3.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting3->AddNetworkRouteTo (Ipv4Address ("10.1.4.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting3->AddNetworkRouteTo (Ipv4Address ("10.1.200.0"), Ipv4Mask ("255.255.255.0"), 2);//interface4.Get(0).second);


        Ptr<Ipv4StaticRouting> staticRouting4 = ipv4RoutingHelper.GetStaticRouting (ipv44);
        // The ifIndex for this outbound route is 1; the first p2p link added
        staticRouting4->AddNetworkRouteTo (Ipv4Address ("10.1.1.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting4->AddNetworkRouteTo (Ipv4Address ("10.1.2.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting4->AddNetworkRouteTo (Ipv4Address ("10.1.3.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting4->AddNetworkRouteTo (Ipv4Address ("10.1.4.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting4->AddNetworkRouteTo (Ipv4Address ("10.1.5.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting4->AddNetworkRouteTo (Ipv4Address ("10.1.6.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);

        Ptr<Ipv4StaticRouting> staticRouting5 = ipv4RoutingHelper.GetStaticRouting (ipv45);
        // The ifIndex for this outbound route is 1; the first p2p link added
        staticRouting5->AddNetworkRouteTo (Ipv4Address ("10.1.1.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting5->AddNetworkRouteTo (Ipv4Address ("10.1.2.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting5->AddNetworkRouteTo (Ipv4Address ("10.1.3.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting5->AddNetworkRouteTo (Ipv4Address ("10.1.4.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting5->AddNetworkRouteTo (Ipv4Address ("10.1.5.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting5->AddNetworkRouteTo (Ipv4Address ("10.1.6.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);

        Ptr<Ipv4StaticRouting> staticRouting6 = ipv4RoutingHelper.GetStaticRouting (ipv46);
        // The ifIndex for this outbound route is 1; the first p2p link added
        staticRouting6->AddNetworkRouteTo (Ipv4Address ("10.1.1.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting6->AddNetworkRouteTo (Ipv4Address ("10.1.2.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting6->AddNetworkRouteTo (Ipv4Address ("10.1.3.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting6->AddNetworkRouteTo (Ipv4Address ("10.1.4.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting6->AddNetworkRouteTo (Ipv4Address ("10.1.5.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting6->AddNetworkRouteTo (Ipv4Address ("10.1.6.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting6->AddNetworkRouteTo (Ipv4Address ("10.1.7.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting6->AddNetworkRouteTo (Ipv4Address ("10.1.8.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);

        Ptr<Ipv4StaticRouting> staticRouting7 = ipv4RoutingHelper.GetStaticRouting (ipv47);
        // The ifIndex for this outbound route is 1; the first p2p link added
        staticRouting7->AddNetworkRouteTo (Ipv4Address ("10.1.1.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting7->AddNetworkRouteTo (Ipv4Address ("10.1.2.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting7->AddNetworkRouteTo (Ipv4Address ("10.1.3.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting7->AddNetworkRouteTo (Ipv4Address ("10.1.4.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting7->AddNetworkRouteTo (Ipv4Address ("10.1.5.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting7->AddNetworkRouteTo (Ipv4Address ("10.1.6.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting7->AddNetworkRouteTo (Ipv4Address ("10.1.7.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
        staticRouting7->AddNetworkRouteTo (Ipv4Address ("10.1.8.0"), Ipv4Mask ("255.255.255.0"), 1);//interface4.Get(0).second);
	*/
	
  // ns3 error models
          //Defining error model                
                // defining rate error model
                Ptr<RateErrorModel> em = CreateObject<RateErrorModel> ();
                em->SetAttribute ("ErrorRate", DoubleValue (varErrorRate));
                em->SetAttribute ("ErrorUnit", StringValue ("ERROR_UNIT_PACKET")); 
               
                // defining burst error model
                Ptr<BurstErrorModel> emBurst = CreateObject<BurstErrorModel> ();
                emBurst->SetAttribute ("ErrorRate", DoubleValue (varErrorRate)); //burst size by default is randomly picked from 1 to 4 packets
                
          //Linking rate error model to p2p device in node-2                
                if( varErrorModel.compare("RateErrorModel") == 0 )
                {
                   devices_p2p_3.Get (1)->SetAttribute ("ReceiveErrorModel", PointerValue (em));
                   devices_p2p_3.Get (0)->SetAttribute ("ReceiveErrorModel", PointerValue (em));
                }

                else if( varErrorModel.compare("BurstErrorModel") == 0 )            
                   devices_p2p_3.Get (1)->SetAttribute ("ReceiveErrorModel", PointerValue (emBurst));

  // ns3 Applications ----------------        
                        ////  On/off application [forward direction]
				std::string varSocketFactoryType = "ns3::UdpSocketFactory";					

				if( varSimulatedTrafficMode.compare("tcp") == 0)						     
					varSocketFactoryType = "ns3::TcpSocketFactory";

                                if( varSimulatedTrafficDirection.compare("fwd") == 0 or varSimulatedTrafficDirection.compare("fwd/bwd") == 0)
                                {                                
                                        uint16_t port = 9;   // Discard port (RFC 863)     				        

					OnOffHelper onoff (varSocketFactoryType, Address (InetSocketAddress ("10.1.6.2", port)));

                                        if( varSimulatedTrafficType.compare("const") == 0 )
                                        {
                                                onoff.SetConstantRate (DataRate (varSimulatedTraffic_Rate), varSimulatedTraffic_PacketSize); // to keep rate const
                                        }
                                        else
                                        { 
                                                onoff.SetAttribute ("PacketSize", UintegerValue (varSimulatedTraffic_PacketSize));
                                                onoff.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
                                                onoff.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
                                                onoff.SetAttribute ("DataRate", StringValue (varSimulatedTraffic_Rate));
                                        } 
                                        // installing on off application          
                                        ApplicationContainer apps = onoff.Install (mynodes.Get(4));
                                        apps.Start (Seconds (1.0));
                                        apps.Stop (Seconds (1000.0)); 
                                        // Create a packet sink to receive these packets
					PacketSinkHelper sink (varSocketFactoryType, Address (InetSocketAddress (Ipv4Address::GetAny (), port)));
                                        ApplicationContainer sinkApps = sink.Install (mynodes.Get(5));
                                        sinkApps.Start (Seconds (1.0));
                                        sinkApps.Stop (Seconds (1000.0)); 
                                }   
                        ////  On/off application [backward direction]
                                if( varSimulatedTrafficDirection.compare("bwd") == 0 or varSimulatedTrafficDirection.compare("fwd/bwd") == 0)
                                {                                
                                        uint16_t port = 9;   // Discard port (RFC 863)          
                                       	OnOffHelper onoff2 (varSocketFactoryType, Address (InetSocketAddress ("10.1.7.1", port)));

                                        if( varSimulatedTrafficType.compare("const") == 0 )
                                        {
                                                onoff2.SetConstantRate (DataRate (varSimulatedTraffic_Rate), varSimulatedTraffic_PacketSize); // to keep rate const
                                        }
                                        else
                                        { 
                                                onoff2.SetAttribute ("PacketSize", UintegerValue (varSimulatedTraffic_PacketSize));
                                                onoff2.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
                                                onoff2.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
                                                onoff2.SetAttribute ("DataRate", StringValue (varSimulatedTraffic_Rate));
                                        } 
                                        // installing on off application          
                                        ApplicationContainer apps2 = onoff2.Install (mynodes.Get(7));
                                        apps2.Start (Seconds (1.0));
                                        apps2.Stop (Seconds (1000.0)); 
					PacketSinkHelper sink2 (varSocketFactoryType, Address (InetSocketAddress (Ipv4Address::GetAny (), port)));
                                        ApplicationContainer sinkApps2 = sink2.Install (mynodes.Get(6));
                                        sinkApps2.Start (Seconds (1.0));
                                        sinkApps2.Stop (Seconds (1000.0)); 
                                }
                                  
                        
                        ////    Ping Application
                                //Configuring client ping application
                                V4PingHelper pingClient("10.1.4.2"); //argument is the remote ip to ping
                                pingClient.SetAttribute("Verbose", BooleanValue (true));
                                //Installing Client Application
                                ApplicationContainer clientApps = pingClient.Install(mynodes.Get(0));
                                clientApps.Start(Seconds(1.0));
                                clientApps.Stop(Seconds(10.0));         
                                //Giving a name to the client ping applicatin
                                Names::Add ("app", clientApps.Get(0));
                                //Hooking a trace to the client ping application
                                Config::Connect ("/Names/app/Rtt", MakeCallback (&PingRtt));
        

  // for debugging
  pointToPoint.EnablePcapAll("first");      

  // KPOL Running the simulation
  Simulator::Stop (Seconds (50000.0)); //need this for emulation
  Simulator::Run ();
  Simulator::Destroy ();
  NS_LOG_INFO ("Done.");
}
