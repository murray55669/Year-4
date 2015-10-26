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
	private List<Integer> n_ids;

	// Queues for the incoming messages
	public List<String> incomingMsg;
	
	//Timings this node will initiate an election
	private List<Integer> elections;
	
	private String nextMsg = "";
	
	public Node(int id){
	
		this.id = id;
		
		myNeighbours = new ArrayList<Node>();
		incomingMsg = new ArrayList<String>();
		
		n_ids = new ArrayList<Integer>();
		elections = new ArrayList<Integer>();
	}
	
	@Override
	public String toString() {
	    return "Node "+this.id;
	}
	
	// Basic methods for the Node class
	
	public int getNodeId() {
		/*
		Method to get the Id of a node instance
		*/
		return this.id;
	}
			
	public boolean isNodeLeader() {
		/*
		Method to return true if the node is currently a leader
		*/
		return leader;
	}
	
	public boolean isNodeParticipant() {
		return participant;
	}
		
	public List<Node> getNeighbors() {
		/*
		Method to get the neighbours of the node
		*/
		return myNeighbours;
	}
		
	public void addNeighbour(Node n) {
		/*
		Method to add a neighbour to a node
		*/
		this.myNeighbours.add(n);
	}
	
	public void add_n_id(int id) {
		n_ids.add(id);
	}
	public List<Integer> dump_n_ids() {
		List<Integer> temp = new ArrayList<Integer>(this.n_ids);
		this.n_ids.clear();
		return temp;
	}
	
	public void add_election(int round) {
		elections.add(round);
	}
	
	public Network getNetwork () {
		return this.network;
	}
				
	public void receiveMsg(String m) {
		/*
		Method that implements the reception of an incoming message by a node
		*/ 
		
		this.incomingMsg.add(m);
		
		String[] chunks = m.split(" ");
		int incId = Integer.parseInt(chunks[1]);
		
		if (chunks[0].equals("ELECTION")) {
			if (!this.participant) {
				//If we are not a participant, become a participant, and send max(m.id, p.id) to next node
				this.participant = true;
				
				int outId = Math.max(incId, this.getNodeId());
				
				this.nextMsg = ("ELECTION "+outId);
			} else {
				
				if (incId == this.getNodeId()) {
					//If we're the new leader, send a message informing the other nodes
					this.participant = false;
					this.leader = true;
					this.nextMsg = ("LEADER "+this.getNodeId());
				} else if (incId < this.getNodeId()) {
					//We have already send an election message with higher id, so do nothing
				} else if (incId > this.getNodeId()) {
					//If inc id is greater than ours, forward the message
					this.nextMsg = ("ELECTION "+incId);
				}
			}
		} else if (chunks[0].equals("LEADER")) {
			if (this.getNodeId() == incId) {
				//If we are the leader, do nothing
			} else {
				//Remove ourselves from the election, forward the leader message
				this.participant = false;
				this.leader = false;
				this.nextMsg = "LEADER "+incId;
			}
		}
	} 
	
	public void sendMsg(String m) {
		/*
		Method that implements the sending of a message by a node. 
		The message must be delivered to its recepients through the network.
		This method need only implement the logic of the network receiving an outgoing message from a node.
		The remainder of the logic will be implemented in the network class.
		*/
		this.network.addMessage(this.id, m);
	}
	
	public void tick(int round) {
		//Send whatever message we have queued
		if (!(this.nextMsg.equals(""))) {
			this.sendMsg(this.nextMsg);
		}
		this.nextMsg = "";
		
		//Start an election if required on this round
		for (Integer election : this.elections) {
			if (round == election) {
				if (this.participant) {
					System.out.println("Node "+this.getNodeId()+" didn't start election; already a participant!");
				} else {
					System.out.println("Node "+this.getNodeId()+" starting election!");
					//Sets own state to participant
					this.participant = true;
					//Send election message to 1st neighbour
					this.sendMsg("ELECTION "+this.getNodeId());
				}
			}
		}
	}

	public void setNetwork(Network net) {
		this.network = net;
	}
}
