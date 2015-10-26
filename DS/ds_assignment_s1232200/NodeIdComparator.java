import java.util.Comparator;

public class NodeIdComparator implements Comparator<Node> {
	public int compare(Node n1, Node n2) {
        return n1.getNodeId() - n2.getNodeId();
    }
}