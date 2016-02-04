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
#include "ns3/flow-monitor-module.h"
#include "ns3/random-variable-stream.h"

#include <string>
#include <vector>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("AssignmentTemplate"); // Doxygen Documentation System

// Declarations
int run_number;
uint64_t throughput [5];
void simulate(int question, bool rayleigh, int aarf_cara, int separation, int node_count);

int FlowOutput(Ptr<FlowMonitor> flowmon, FlowMonitorHelper *flowmonHelper)
{
  flowmon->CheckForLostPackets (); //check all packets have been sent or completely lost
  Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowmonHelper->GetClassifier ());
  std::map<FlowId, FlowMonitor::FlowStats> stats = flowmon->GetFlowStats (); // pull stats from flow monitor

  uint64_t total = 0;
  
  for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator iter = stats.begin (); iter != stats.end (); ++iter)
  {
    total += iter->second.rxBytes;
    throughput[run_number] = (total);
  }
  return 0;
}

int main (int argc, char *argv[]) {
  bool verbose = false;
  
  int question = 0;
  bool rayleigh = false;
  int aarf_cara = 0; // aarf = 0, cara = 1
  int separation = 0;
  int node_count = 0; //station nodes
  
  CommandLine cmd;
  cmd.AddValue ("verbose", "Tell echo applications to log if true", verbose); //parameter name, description, variable that will take the value read from the command line
  cmd.AddValue ("question", "Question number (1-3)", question);
  cmd.AddValue ("rayleigh", "Rayleigh (true or false)", rayleigh);
  cmd.AddValue ("aarfcara", "AARF or CARA (0 or 1 respectively)", aarf_cara);
  cmd.AddValue ("separation", "Separation", separation);
  cmd.AddValue ("nodecount", "Node count", node_count);

  cmd.Parse (argc,argv);
  
  NS_LOG_UNCOND("Question: " << question << "; Rayleigh: " << rayleigh << "; AARF/CARA: " << aarf_cara << "; Separation: " << separation << "; Node count: " << node_count);
  
  if (verbose)
    {
      LogComponentEnable ("PacketSink", LOG_LEVEL_INFO); //packet sink should write all actions to the command line
    }
    
  for (run_number = 0; run_number < 5; ++run_number) {
    SeedManager::SetSeed (run_number+1);//seed number should change between runs if running multiple simulations.
    simulate(question, rayleigh, aarf_cara, separation, node_count);
  }
  
  uint64_t total = 0;
  for (int i = 0; i < 5; ++i) {
    total += throughput[i];
  }
  NS_LOG_UNCOND("Average: " << ((total * 8.0 / (10 * 1024)) / 5));
  
  return 0;
}

void simulate (int question, bool rayleigh, int aarf_cara, int separation, int node_count)
{
  // Generate nodes
  NodeContainer wifiStaNodes; //create AP Node and (one or more) Station node(s)
  wifiStaNodes.Create (node_count);
  NodeContainer wifiApNode;
  wifiApNode.Create(1); 
  // Set up physical layer
  YansWifiChannelHelper channel; //create helpers for the channel and phy layer and set propagation configuration here.
  channel.SetPropagationDelay ("ns3::ConstantSpeedPropagationDelayModel");
  channel.AddPropagationLoss("ns3::LogDistancePropagationLossModel");
  if(rayleigh){
    channel.AddPropagationLoss("ns3::NakagamiPropagationLossModel",
	                           "m0", DoubleValue(1.0), "m1", DoubleValue(1.0), "m2", DoubleValue(1.0)); //combining log and nakagami to have both distance and rayleigh fading (nakami with m0, m1 and m2 =1 is rayleigh)
  }
  YansWifiPhyHelper phy = YansWifiPhyHelper::Default ();
  phy.SetChannel (channel.Create ());
  
  // Set up wifi
  WifiHelper wifi = WifiHelper::Default (); //create helper for the overall wifi setup and configure a station manager
  wifi.SetStandard(ns3::WIFI_PHY_STANDARD_80211g);
  if (aarf_cara == 1) {
    wifi.SetRemoteStationManager ("ns3::CaraWifiManager");
  } else if (aarf_cara == 0) {
    wifi.SetRemoteStationManager ("ns3::AarfWifiManager"); 
  } else {
    NS_LOG_UNCOND("Invalid AARF/CARA");
    return;
  }
  NqosWifiMacHelper mac = NqosWifiMacHelper::Default (); //create a mac helper and configure for station and AP and install
  Ssid ssid = Ssid ("example-ssid");
  mac.SetType ("ns3::StaWifiMac",
               "Ssid", SsidValue (ssid),
               "ActiveProbing", BooleanValue (false));
               
  // Add nodes 
  NetDeviceContainer staDevices;
  staDevices = wifi.Install (phy, mac, wifiStaNodes);

  mac.SetType ("ns3::ApWifiMac",
               "Ssid", SsidValue (ssid));

  NetDeviceContainer apDevices;
  apDevices = wifi.Install (phy, mac, wifiApNode);
  MobilityHelper mobility;
  // Position nodes
  switch(question) {
    case 0:
      NS_LOG_UNCOND("Invalid question!");
      return;
      break;
    case 1: 
      mobility.SetPositionAllocator ("ns3::GridPositionAllocator", //places nodes in a grid with distance between nodes and grid width defined below, for 2 nodes can be used to easily place them at a set distance apart
                                 "MinX", DoubleValue (0.0), //first node positioned at x = 0, y= 0
                                 "MinY", DoubleValue (0.0),
                                 "DeltaX", DoubleValue (separation), //nodes will be place 5m apart in x plane
                                 "DeltaY", DoubleValue (0.0),
                                 "GridWidth", UintegerValue (3), 
                                 "LayoutType", StringValue ("RowFirst"));
      break;
    case 2: 
      mobility.SetPositionAllocator ("ns3::RandomDiscPositionAllocator", 
                                     "Rho", StringValue ("ns3::UniformRandomVariable[Min=10|Max=10]"),
                                     "X", DoubleValue (0.0), 
                                     "Y", DoubleValue (0.0));
      break;
    case 3: 
      mobility.SetPositionAllocator ("ns3::RandomDiscPositionAllocator", 
                                     "Rho", StringValue ("ns3::UniformRandomVariable[Min=0.1|Max=25]"),
                                     "X", DoubleValue (0.0), 
                                     "Y", DoubleValue (0.0));
      break;
  }
  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel"); //nodes shouldn't move once placed
  mobility.Install (wifiApNode);
  mobility.Install (wifiStaNodes);

  // Install internet stack
  InternetStackHelper stack; //install the internet stack on both nodes
  stack.Install (wifiApNode);
  stack.Install (wifiStaNodes);

  // Assign IPs
  Ipv4AddressHelper address; //assign IP addresses to all nodes
  address.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer apAddress = address.Assign (apDevices); //we need to keep AP address accessible as we need it later
  Ipv4InterfaceContainer staAddress = address.Assign (staDevices);
  
  // Set up senders/receivers 
  std::string dataRate = "20Mib/s"; //data rate set as a string, see documentation for accepted units
  
  double min = 0.0;
  double max = 0.1;
  Config::SetDefault ("ns3::UniformRandomVariable::Min", DoubleValue (min));
  Config::SetDefault ("ns3::UniformRandomVariable::Max", DoubleValue (max));
  Ptr<UniformRandomVariable> var = CreateObject<UniformRandomVariable> ();
  
  std::vector<OnOffHelper> onoffs;
  std::vector<ApplicationContainer> apps;
  
  for (int i = 0; i < node_count; ++i) {
    OnOffHelper onoff ("ns3::UdpSocketFactory", Address ()); //create a new on-off application to send data
    onoff.SetConstantRate(dataRate, (uint32_t)1024); //set the onoff client application to CBR mode
    
    if (var->GetValue(0, 1.0) > 0.5) // Randomly assign sender/receiver roles 
    {
      AddressValue remoteAddress (InetSocketAddress (apAddress.GetAddress (0), 8000)); //specify address and port of the AP as the destination for on-off application's packets
      onoff.SetAttribute ("Remote", remoteAddress);
      ApplicationContainer app = onoff.Install (wifiStaNodes.Get (i));//install onoff application on stanode 0 and configure start/stop times

      app.Start(Seconds(var->GetValue(0, 0.1)));
      app.Stop (Seconds (10.0));
      PacketSinkHelper sink("ns3::UdpSocketFactory", InetSocketAddress (apAddress.GetAddress (0), 8000)); //create packet sink on AP node with address and port that on-off app is sending to
      app.Add(sink.Install(wifiApNode.Get(0)));
      
      onoffs.push_back(onoff);
      apps.push_back(app);
    } else {
      AddressValue remoteAddress (InetSocketAddress (staAddress.GetAddress (i), 8000));
      onoff.SetAttribute ("Remote", remoteAddress);
      ApplicationContainer app = onoff.Install (wifiApNode.Get (0));

      app.Start(Seconds(var->GetValue(0, 0.1)));
      app.Stop (Seconds (10.0));
      PacketSinkHelper sink("ns3::UdpSocketFactory", InetSocketAddress (staAddress.GetAddress (i), 8000)); //create packet sink on AP node with address and port that on-off app is sending to
      app.Add(sink.Install(wifiStaNodes.Get(i)));
      
      onoffs.push_back(onoff);
      apps.push_back(app);
    }
  }

  Simulator::Stop (Seconds (10.0)); //define stop time of simulator

  Ptr<FlowMonitor> flowmon; //create an install a flow monitor to monitor all transmissions around the network
  FlowMonitorHelper *flowmonHelper = new FlowMonitorHelper();
  flowmon = flowmonHelper->InstallAll();

  Simulator::Run (); //run the simulation and destroy it once done
  Simulator::Destroy ();
  FlowOutput(flowmon, flowmonHelper);
}
