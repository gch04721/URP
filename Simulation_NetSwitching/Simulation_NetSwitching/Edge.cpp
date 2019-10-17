#include "Edge.h"
#include "Node.h"
#include "Connection.h"

Edge::Edge(double x, double y, int no) {
	this->no = no;
	this->x = x;
	this->y = y;
	this->dataQueue = 0;
	this->isOvered = false;
}

/*
Node를 연결하는 상황에서 연결리스트에 추가해주고 데이터 큐만큼 더해줌.
이 함수는 Node의 데이터 생성(generateData) 완료 이후에 불려져야함.
*/
void Edge::newConnect(Node* node, int type) {
	this->connectedList.push_back(new Connection(node, type));
	node->setProcessSize();
	if (node->connectType == 1) {
		this->dataQueue += node->processSize;
	}
	else if (node->connectType == 2) {
		if (node->dataQueue > 60)
			this->dataQueue += 60;
		else
			this->dataQueue += node->dataQueue;
	}
	else {
		this->dataQueue += node->processSize;
	}
	if (this->dataQueue > 100) isOvered = true;
}

// 특정 Node를 제거해준다. Node의 데이터 생성 완료 이후에 불려져야함.
void Edge::disConnectNode(Node* node) {
	for (size_t i = 0; i < this->connectedList.size(); i++) {
		if (this->connectedList[i]->node == node) {
			this->connectedList.erase(this->connectedList.begin() + i);
			break;
		}
	}
	node->setProcessSize();
	this->dataQueue -= node->processSize;
	if (this->dataQueue < 0) this->dataQueue = 0;
	if (this->dataQueue < 100) this->isOvered = false;
}

// 이 Edge device의 Data queue를 안정화시킴. 만약 Over되어있는 경우 처리함.
void Edge::stabilizeQueue() {
	while (isOvered) {
		Node* abandonNode = this->leastPreferNode();
		this->disConnectNode(abandonNode);
		abandonNode->disConnected();
	}
}

// 이 Edge device에 연결된 Node들 중 가장 선호도가 낮은 노드를 선택
Node* Edge::leastPreferNode() {
	double min = DBL_MAX;
	int leastIndex = -1;
	for (size_t i = 0; i < this->connectedList.size(); i++) {
		double preference = this->connectedList[i]->node->connectedPreference;
		if (min > preference) {
			min = preference;
			leastIndex = i;
		}
	}
	return this->connectedList[leastIndex]->node;
}

// 한 Time slot이 종료된 경우 호출
void Edge::timeOver() {
	vector<Connection*>().swap(this->connectedList);
	this->dataQueue = 0;
	this->isOvered = false;
}