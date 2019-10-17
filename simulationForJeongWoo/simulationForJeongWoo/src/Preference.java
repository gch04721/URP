public class Preference {
    public Node node;
    public Edge edge;
    public double preference;
    public int type;

    public Preference(Node node, Edge edge, int type) {
        this.node = node;
        this.edge = edge;
        this.type = type;
        this.preference = getPreference();
    }
    public Preference(Node node, Edge edge, boolean BLE){
        this.node = node;
        this.edge = edge;
        this.preference = getPreference(BLE);
    }

    // TODO : Preference 계산 결과 넣어주기
    public double getPreference() {
        return 0.0;
    }

    public double getPreference(boolean BLE){
        double min;
        if(BLE){
            node.connectType = 1;
            node.setProcessSize();
            double p_ble = 0.0076 * Math.log(node.processSize * 100) + 0.01;
            double q_ble = node.dataQueue - node.processSize;
            if(q_ble < 0)
                q_ble =0.0;

            node.connectType = 2;
            node.setProcessSize();
            double p_wifi = 210.0;
            double q_wifi = node.dataQueue - node.processSize;
            if(q_wifi < 0)
                q_wifi = 0.0;

            double v = 10.0;

            min = p_ble + v * q_ble;

            if(min > (p_wifi + v * q_wifi)){
                min = p_wifi + v * q_wifi;
                type = 2;
            }
            else{
                type = 1;
            }
            node.connectType = 0;
            node.setProcessSize();
        }
        else{
            node.connectType = 2;
            node.setProcessSize();
            double p_wifi = 210.0;
            double q_wifi = node.dataQueue - node.processSize;
            if(q_wifi < 0)
                q_wifi = 0.0;

            double v = 10.0;
            min = p_wifi + v * q_wifi;
            node.connectType = 0;
            node.setProcessSize();
            this.type = 2;
        }
        return min;
    }
}
