import java.util.ArrayList;

public class Edge {
    public int no;
    public double x;
    public double y;

    public double dataQueue;
    public boolean isOvered;

    public ArrayList<Connection> connectedList;

    public Edge(double x, double y, int no) {
        this.no = no;
        this.x = x;
        this.y = y;
        dataQueue = 0;
        connectedList = new ArrayList<Connection>();
        isOvered = false;
    }

    // Node를 연결하는 상황에 대해, 연결 리스트에 추가해주고 데이터 큐만큼 더해준다.
    // 이 때 이 함수와 아래의 disconnectNode 함수는 반드시 Node의 데이터 생성 (newData)이 완료된 후에 호출되야 함에 유의할 것.
    public void newConnect(Node node, int type) {
        connectedList.add(new Connection(node, type));
        node.setProcessSize();
        dataQueue += node.processSize;
        if (dataQueue > 100) isOvered = true;
    }

    // 특정 Node를 제거해준다.
    public void disconnectNode(Node node) {
        for (int i = 0; i < connectedList.size(); i++) {
            if (connectedList.get(i).node.equals(node)) {
                connectedList.remove(i);
                break;
            }
        }
        node.setProcessSize();
        dataQueue -= node.processSize;
        if (dataQueue < 0) dataQueue = 0;
        if (dataQueue < 100) isOvered = false;
    }

    // 이 Edge device의 Data Queue를 안정화시킨다. 만약 Over되어 있는 경우 처리한다.
    public void stabilizeQueue() {
        while (isOvered) {
            Node abandonNode = leastPreferNode();
            disconnectNode(abandonNode);
            abandonNode.disConnected();
        }
    }

    // 본인에게 연결된 Node들 중 가장 선호도가 낮은 노드를 선택해서 리턴해준다.
    public Node leastPreferNode() {
        double min = 1000;
        int leastIndex = -1;
        for (int i = 0; i < connectedList.size(); i++) {
            if (min > connectedList.get(i).node.connectPreference) {
                min = connectedList.get(i).node.connectPreference;
                leastIndex = i;
            }
        }

        return connectedList.get(leastIndex).node;
    }

    // 한 Time Slot이 종료된 경우 호출되는 함수.
    public void timeOver() {
        connectedList.clear();
        dataQueue = 0;
        isOvered = false;
    }
}
