import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class Main {
    public static double BLUETOOTH_DIST = 10;

    public static ArrayList<Node> nodeList = new ArrayList<Node>();
    public static ArrayList<Edge> edgeList = new ArrayList<Edge>();

    public static void main(String[] args) throws IOException {
        setUpEnvironment();
        BufferedWriter connectionInfo = new BufferedWriter(new FileWriter("connectionInfo.txt", true));
        BufferedWriter edgeDataQueue = new BufferedWriter(new FileWriter("edgeDataQueue.txt", true));
        BufferedWriter nodeDataQueue = new BufferedWriter(new FileWriter("nodeDataQueue.txt", true));
        BufferedWriter processSize = new BufferedWriter(new FileWriter("processSize.txt", true));

        for(int k =0; k< 3600; k++){
            for (int i = 0; i < nodeList.size(); i++) {
                nodeList.get(i).setInputSize();
                nodeList.get(i).newData();
            }
    
            for (int i = 0; i < nodeList.size(); i++) {
                for (int j = 0; j < edgeList.size(); j++) {
                    // if (getDistance(nodeList.get(i), edgeList.get(j)) <= BLUETOOTH_DIST) {
                    //     nodeList.get(i).addPreferenceList(new Preference(nodeList.get(i), edgeList.get(j), 1));
                    // }
                    // nodeList.get(i).addPreferenceList(new Preference(nodeList.get(i), edgeList.get(j), 2));
                    boolean BLE = getDistance(nodeList.get(i), edgeList.get(j)) <= BLUETOOTH_DIST;
                    nodeList.get(i).addPreferenceList(new Preference(nodeList.get(i), edgeList.get(j), BLE));
                }
            }
    
            /*for (int i = 0; i < nodeList.size(); i++) {
                System.out.println("Node "+nodeList.get(i).no+"번의 선호 리스트 -> Data Queue Size : "+nodeList.get(i).dataQueue);
                for(int a=0;a<nodeList.get(i).preferenceList.size();a++){
                    System.out.println(nodeList.get(i).preferenceList.get(a).edge.no + "번 엣지와 "+nodeList.get(i).preferenceList.get(a).type +
                            "타입의 통신에 대한 선호도 : "+nodeList.get(i).preferenceList.get(a).preference);
                }
            }*/
    
            for (int i = 0; i < nodeList.size(); i++) {
                nodeList.get(i).connectMostPreferEdge();
            }
    
            /*for (int i = 0; i < nodeList.size(); i++) {
                System.out.println("Node " + nodeList.get(i).no + "번의 연결 엣지 : " + nodeList.get(i).connectedEdge.no);
                }
            }*/
    
            for (int j = 0; j < edgeList.size(); j++) {
                edgeList.get(j).stabilizeQueue();
            }
    
            while (!isFinished()) {
                for (int i = 0; i < nodeList.size(); i++) {
                    if (!nodeList.get(i).isConnected) {
                        nodeList.get(i).connectMostPreferEdge();
                        if(nodeList.get(i).connectType != 0){
                            nodeList.get(i).connectedEdge.stabilizeQueue();
                        }
                    }
                }
            }
    
            for (int i = 0; i < nodeList.size(); i++) {
                if(nodeList.get(i).connectType != 0){
                    System.out.println("Node " + nodeList.get(i).no + "번의 연결 엣지 : " + nodeList.get(i).connectedEdge.no);
                }
            }
            System.out.println("");
            
            // 각 Timeslot마다 
            // Node와 Edge의 연결관계
            // Node의 data queue
            // Edge의 data queue
            // Node의 processing size
            String _connectionInfo, edgeDataQueueInfo, nodeDataQueueInfo, processSizeInfo;
            for(int i =0; i < 15; i++){
                if(nodeList.get(i).connectedEdge == null)
                    _connectionInfo = "(" + nodeList.get(i).no + "," + -1 + "," + nodeList.get(i).connectType + ")";    
                else
                    _connectionInfo = "(" + nodeList.get(i).no + "," + nodeList.get(i).connectedEdge.no + "," + nodeList.get(i).connectType + ")";
                if(i < 5){
                    edgeDataQueueInfo = Double.toString(edgeList.get(i).dataQueue);
                    edgeDataQueue.write(edgeDataQueueInfo);
                    edgeDataQueue.newLine();
                }
                nodeDataQueueInfo = Double.toString(nodeList.get(i).dataQueue);
                processSizeInfo = Double.toString(nodeList.get(i).processSize);

                connectionInfo.write(_connectionInfo);
                connectionInfo.newLine();
                
                nodeDataQueue.write(nodeDataQueueInfo);
                nodeDataQueue.newLine();

                processSize.write(processSizeInfo);
                processSize.newLine();
            }
            connectionInfo.newLine();
            edgeDataQueue.newLine();
            nodeDataQueue.newLine();
            processSize.newLine();

            for (int i = 0; i < nodeList.size(); i++) {
                nodeList.get(i).setProcessSize();
                nodeList.get(i).timeOver();
            }
            for (int j = 0; j < edgeList.size(); j++) {
                edgeList.get(j).timeOver();
            }

        }
        connectionInfo.close();
        edgeDataQueue.close();
        nodeDataQueue.close();
        processSize.close();
    }

    public static void setUpEnvironment(){
        nodeList.add(new Node(3, 13, 1, false));
        nodeList.add(new Node(31, 9, 2, false));
        nodeList.add(new Node(18, 12, 3, false));
        nodeList.add(new Node(18, 17, 4, true));
        nodeList.add(new Node(22, 18, 5, false));
        nodeList.add(new Node(16, 20, 6, false));
        nodeList.add(new Node(13, 22, 7, true));
        nodeList.add(new Node(12, 28, 8, false));
        nodeList.add(new Node(26, 32, 9, true));
        nodeList.add(new Node(28, 30, 10, true));
        nodeList.add(new Node(23, 32, 11, false));
        nodeList.add(new Node(18, 34, 12, false));
        nodeList.add(new Node(43, 38, 13,true));
        nodeList.add(new Node(27, 38, 14, false));
        nodeList.add(new Node(17, 47, 15, false));

        edgeList.add(new Edge(25, 10, 1));
        edgeList.add(new Edge(10, 15, 2));
        edgeList.add(new Edge(20, 25, 3));
        edgeList.add(new Edge(20, 40, 4));
        edgeList.add(new Edge(35, 35, 5));
    }

    public static double getDistance(Node node, Edge edge) {
        return Math.sqrt(Math.pow((node.x - edge.x), 2) + Math.pow((node.y - edge.y), 2));
    }

    public static boolean isFinished() {
        for (int i = 0; i < nodeList.size(); i++) {
            if (!nodeList.get(i).isConnected) {
                return false;
            }
        }
        return true;
    }
}
