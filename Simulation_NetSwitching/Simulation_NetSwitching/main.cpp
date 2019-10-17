#include <iostream>
#include <random>
#include <vector>
#include <fstream>

#include "Node.h"
#include "Edge.h"
#include "Connection.h"
#include "Preference.h"

#define BLUETOOTH_DIST 10

using namespace std;
void setUpEnv(vector<Node*>& nodeList, vector<Edge*>& edgeList);
double getDistance(Node* ndoe, Edge* edge);
bool isFinished(vector<Node*> nodeList);

int main() {
	// data 기록용
	ofstream connectionInfo, edgeDataQueueInfo, nodeDataQueueInfo, processSizeInfo;
	connectionInfo.open("..\\..\\dataAnalysis\\connectionInfo.txt", ios::out | ios::trunc);
	nodeDataQueueInfo.open("..\\..\\dataAnalysis\\nodeDataQueue.txt", ios::out | ios::trunc);
	edgeDataQueueInfo.open("..\\..\\dataAnalysis\\edgeDataQueue.txt", ios::out | ios::trunc);
	processSizeInfo.open("..\\..\\dataAnalysis\\processSize.txt", ios::out | ios::trunc);

	// poisson distribution을 따르는 난수 생성기
	std::default_random_engine gen;
	std::poisson_distribution<int> distribution(15);
	
	vector<Node*> nodeList;
	vector<Edge*> edgeList;

	setUpEnv(nodeList, edgeList);
	for (int timeSlot = 0; timeSlot < 3600; timeSlot++) {
		// 각 node가 데이터 생성
		for (size_t i = 0; i < nodeList.size(); i++) {
			int dataSize = distribution(gen);
			cout << "data : " << dataSize << endl;
			nodeList[i]->setInputSize(dataSize);
			nodeList[i]->generateData();
		}

		// 각 node가 Edge별 선호도 계산
		for (size_t i = 0; i < nodeList.size(); i++) {
			for (size_t j = 0; j < edgeList.size(); j++) {
				bool checkBLE = (getDistance(nodeList[i], edgeList[j]) <= BLUETOOTH_DIST);
				nodeList[i]->addPreferenceList(new Preference(nodeList[i], edgeList[j], checkBLE));
			}
		}

		// 선호도를 기반으로 연결 수행
		for (size_t i = 0; i < nodeList.size(); i++) {
			nodeList[i]->connectMostPreferEdge();
		}

		// 각 edge들이 queue에 따라 필요시 연결 해제 시도
		for (size_t i = 0; i < edgeList.size(); i++) {
			edgeList[i]->stabilizeQueue();
		}

		// 큐 안정화로 인해 연결이 해제된 node들을 다음 선호도를 가지는 edge에 연결 시도
		while (!isFinished(nodeList)) {
			for (size_t i = 0; i < nodeList.size(); i++) {
				if (!nodeList[i]->isConnected) {
					nodeList[i]->connectMostPreferEdge();
					if (nodeList[i]->connectType != 0) {
						nodeList[i]->connectedEdge->stabilizeQueue();
					}
				}
			}
		}

		// 연결상태 출력
		for (size_t i = 0; i < edgeList.size(); i++) {
			cout << edgeList[i]->no << "번의 연결 노드 : ";
			for (size_t j = 0; j < edgeList[i]->connectedList.size(); j++) {
				cout << edgeList[i]->connectedList[j]->node->no << " ";
			}
			cout << endl;
		}
		cout << "연결되지 않은 노드 : ";
		for (size_t i = 0; i < nodeList.size(); i++) {
			if (nodeList[i]->connectType == 0)
				cout << nodeList[i]->no << " ";
		}
		cout << endl;

		// 현재 Timeslot에서 생성량과 송신량 처리

		for (size_t i = 0; i < nodeList.size(); i++)
			nodeList[i]->setProcessSize();

		// 데이터 기록
		for (size_t i = 0; i < nodeList.size(); i++) {
			if (i < edgeList.size()) {
				edgeDataQueueInfo << edgeList[i]->dataQueue << endl;
			}
			if (nodeList[i]->connectedEdge == nullptr) {
				connectionInfo << "(" << nodeList[i]->no << "," << -1 << "," << nodeList[i]->connectType << ")" << endl;
			}
			else {
				connectionInfo << "(" << nodeList[i]->no << "," << nodeList[i]->connectedEdge->no << "," << nodeList[i]->connectType << ")" << endl;
			}
			nodeDataQueueInfo << nodeList[i]->dataQueue << endl;
			processSizeInfo << nodeList[i]->processSize << endl;
		}

		// 현재 time slot 종료
		for (size_t i = 0; i < nodeList.size(); i++)
			nodeList[i]->timeOver();
		for (size_t i = 0; i < edgeList.size(); i++)
			edgeList[i]->timeOver();
	}
	connectionInfo.close();
	nodeDataQueueInfo.close();
	edgeDataQueueInfo.close();
	processSizeInfo.close();
	return 0;
}

void setUpEnv(vector<Node*>& nodeList, vector<Edge*>& edgeList) {
	nodeList.push_back(new Node(3, 13, 1, false));
	nodeList.push_back(new Node(31, 9, 2, false));
	nodeList.push_back(new Node(18, 12, 3, false));
	nodeList.push_back(new Node(18, 17, 4, true));
	nodeList.push_back(new Node(22, 18, 5, false));
	nodeList.push_back(new Node(16, 20, 6, false));
	nodeList.push_back(new Node(13, 22, 7, true));
	nodeList.push_back(new Node(12, 28, 8, false));
	nodeList.push_back(new Node(26, 32, 9, true));
	nodeList.push_back(new Node(28, 30, 10, true));
	nodeList.push_back(new Node(23, 32, 11, false));
	nodeList.push_back(new Node(18, 34, 12, false));
	nodeList.push_back(new Node(43, 38, 13, true));
	nodeList.push_back(new Node(27, 38, 14, false));
	nodeList.push_back(new Node(17, 47, 15, false));

	edgeList.push_back(new Edge(25, 10, 1));
	edgeList.push_back(new Edge(10, 15, 2));
	edgeList.push_back(new Edge(20, 25, 3));
	edgeList.push_back(new Edge(20, 40, 4));
	edgeList.push_back(new Edge(35, 35, 5));
}

double getDistance(Node* node, Edge* edge) {
	return sqrt(pow((node->x - edge->x), 2) + pow(node->y - edge->y, 2));
}

bool isFinished(vector<Node*> nodeList) {
	for (size_t i = 0; i < nodeList.size(); i++) {
		if (!nodeList[i]->isConnected)
			return false;
	}
	return true;
}