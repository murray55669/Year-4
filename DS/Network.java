import java.util.*;
import java.io.*;

/* 
Class to simulate the network. System design directions:

- Synchronous communication: each round lasts for 20ms
- At each round the network receives the messages that the nodes want to send and delivers them
- The network should make sure that:
	- A node can only send messages to its neighbours
	- A node can only send one message per neighbour per round
- When a node fails, the network must inform all the node's neighbours about the failure
*/

public class Network {

	private static List<Node> nodes;
	private int round;
	private int period = 20;
	private Map<Integer, String> msgToDeliver; //Integer for the id of the sender and String for the message
	
	public NetSimulator() {
        	msgToDeliver = new HashMap<Integer, String>();
        	
        	/*
        	Code to call methods for parsing the input file, initiating the system and producing the log can be added here.
        	*/
   		}
   		
   	private parseFile(String fileName) throws IOException {
   		/*
   		Code to parse the file can be added here. Notice that the method's descriptor must be defined.
   		*/
   		}
	
	public synchronized void addMessage(int id, String m) {
		/*
		At each round, the network collects all the messages that the nodes want to send to their neighbours. 
		Implement this logic here.
		*/
		}
	
	public synchronized void deliverMessages() {
		/*
		At each round, the network delivers all the messages that it has collected from the nodes.
		Implement this logic here.
		The network must ensure that a node can send only to its neighbours, one message per round per neighbour.
		*/
		}
		
	public synchronized void informNodeFailure(int id) {
		/*
		Method to inform the neighbours of a failed node about the event.
		*/
		}
	
	
	public static void main(String args[0]) throws IOException, InterruptedException {
		/*
		Your main must get the input file as input.
		*/
		}
	
	
	
	
	
	
	
}
