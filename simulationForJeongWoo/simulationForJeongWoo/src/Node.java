import java.util.ArrayList;
import java.util.Random;

public class Node {
    public int no;
    public double x;
    public double y;

    public double dataQueue;
    public double inputSize;
    public double processSize;

    public Edge connectedEdge;
    public int connectType;         // 0이면 연결 안됨, 1이면 Bluetooth, 2이면 WiFi
    public boolean isConnected;
    public double connectPreference;

    public boolean bigData;

    public ArrayList<Preference> preferenceList;

    public Node(double x, double y, int no, boolean big) {
        this.no = no;
        this.x = x;
        this.y = y;
        this.bigData = big;
        dataQueue = 0;
        connectType = 0;
        connectPreference=0;
        isConnected = false;
        preferenceList = new ArrayList<Preference>();

        setInputSize();
    }

    // TODO : Input Size 각 노드별로 설정해 줘야 함. 랜덤으로?
    // Gaussian분포를 가지는 난수 생성
    public void setInputSize() {
        // 단위시간동안 생산되는 데이터 총량
        // inputSize 1 = 약 100Kbit, 최대 10000Kbit 데이터 저장 가능
        Random rand = new Random();
        this.inputSize = rand.nextGaussian();
        if(this.inputSize < 0)
            this.inputSize = -1 * this.inputSize;
        this.inputSize *= 4;

        if(this.bigData){
            if(this.inputSize > 3.0){
                this.inputSize = rand.nextGaussian();
                if(this.inputSize < 0)
                    this.inputSize = -1 * this.inputSize;
                this.inputSize = 20 + this.inputSize * 20;
                if(this.inputSize > 50)
                    this.inputSize = 50.0;
                // if(this.dataQueue + this.inputSize > 100.0){
                //     this.inputSize = 99.8 - this.dataQueue;
                // }
            }
        }
    }

    // TODO : Process Size 각 노드별로 설정해 줘야 함. Wi-Fi인지, BLE인지에 따라 판단해 줘야겠지?
    public void setProcessSize() {
        if (connectType == 0) {
            processSize = 0.0;
        } else if (connectType == 1) {
            // BLE
            processSize = this.dataQueue;
            if(processSize >= 1.28)
                processSize = 1.28 ;
        } else {
            // WIFI
            processSize = 60.0; // WIFI는 고정된 값을 가짐
            // 6000Kbit 데이터 처리
        }
    }

    // 새로운 Time Slot에 데이터를 생성해준다. 이 함수가 호출되기 전에 setInputSize를 통해 변수가 지정되었는지 확인해야 함.
    public void newData() {
        dataQueue += inputSize;
        checkOver();
    }

    // 한 Time Slot이 종료되면, 데이터 처리량을 계산해준다. 이 함수가 호출되기 전에 setProcessSize를 통해 변수가 지정되었는지 확인해야 함.
    // 또한 이는 newData보다 먼저 호출되야 함에 유의할 것!
    public void processData() {
        dataQueue -= processSize;
        if (dataQueue < 0) dataQueue = 0;
    }

    // 선호도를 집어넣어 준다.
    public void addPreferenceList(Preference preference) {
        preferenceList.add(preference);
    }

    // 본인의 선호도 리스트 중 가장 선호도가 높은 Edge에 연결을 진행하는 함수.
    public void connectMostPreferEdge() {
        if (preferenceList.size() == 0) {
            isConnected = true;
            connectedEdge = null;
            connectType = 0;
            connectPreference=0;
        } else {
            double max = -1;
            int index = -1;

            for (int i = 0; i < preferenceList.size(); i++) {
                if (preferenceList.get(i).preference > max) {
                    max = preferenceList.get(i).preference;
                    index = i;
                }
            }
            connectedEdge = preferenceList.get(index).edge;
            connectType = preferenceList.get(index).type;
            connectPreference = preferenceList.get(index).preference;
            connectedEdge.newConnect(this, connectType);
            isConnected = true;
        }
    }

    // Edge에 의해 연결이 끊어지는 경우 호출되는 함수.
    public void disConnected() {
        for (int i = 0; i < preferenceList.size(); i++){
            if (preferenceList.get(i).edge.equals(connectedEdge)) {
                preferenceList.remove(i);
            }
        }
        connectedEdge = null;
        connectType = 0;
        connectPreference=0;
        isConnected = false;
    }

    // 노드의 Data Queue가 초과되었는지 체크하여 에러를 표기하는 함수.
    public void checkOver() {
        if (dataQueue > 110) {
            System.out.println("Node " + this.no + "번의 노드\n" + "Error : Node의 data overflow 발생!");
        }
    }

    // 한 Time Slot이 종료된 경우 호출되는 함수.
    public void timeOver() {
        processData();
        preferenceList.clear();

        isConnected = false;
        connectType = 0;
        connectPreference=0;
        connectedEdge = null;
    }
}
