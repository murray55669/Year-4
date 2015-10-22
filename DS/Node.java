import java.util.*;
import java.io.*;

/* Class to represent a node. Each node must run on its own thread.*/

public class Node extends Thread {

	private int id;
	private boolean participant = false;
	private boolean leader = false;
	private Network network;
	
	// Neighbouring nodes
	public List<Node> myNeighbours;

	// Queues for the incoming messages
	public List<String> incomingMsg;
	
	public Node(int id){
	
		this.id = id;
		this.network = network;
		
		myNeighbours = new ArrayList<Node>();
		incomingMsg = new ArrayList<String>();
	}
	
	// Basic methods for the Node class
	
	public int getNodeId() {
		/*
		Method to get the Id of a node instance
		*/
		}
			
	public boolean isNodeLeader() {
		/*
		Method to return true if the node is currently a leader
		*/
		}
		
	public List<Node> getNeighbors() {
		/*
		Method to get the neighbours of the node
		*/
		}
		
	public void addNeighbour(Node n) {
		/*
		Method to add a neighbour to a node
		*/
		}
				
	public void receiveMsg(String m) {
		/*
		Method that implements the reception of an incoming message by a node
		*/
		}
		
	public void sendMsg(String m) {
		/*
		Method that implements the sending of a message by a node. 
		The message must be delivered to its recepients through the network.
		This method need only implement the logic of the network receiving an outgoing message from a node.
		The remainder of the logic will be implemented in the network class.
		*/		
		}
	
}
