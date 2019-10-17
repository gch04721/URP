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
Node�� �����ϴ� ��Ȳ���� ���Ḯ��Ʈ�� �߰����ְ� ������ ť��ŭ ������.
�� �Լ��� Node�� ������ ����(generateData) �Ϸ� ���Ŀ� �ҷ�������.
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

// Ư�� Node�� �������ش�. Node�� ������ ���� �Ϸ� ���Ŀ� �ҷ�������.
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

// �� Edge device�� Data queue�� ����ȭ��Ŵ. ���� Over�Ǿ��ִ� ��� ó����.
void Edge::stabilizeQueue() {
	while (isOvered) {
		Node* abandonNode = this->leastPreferNode();
		this->disConnectNode(abandonNode);
		abandonNode->disConnected();
	}
}

// �� Edge device�� ����� Node�� �� ���� ��ȣ���� ���� ��带 ����
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

// �� Time slot�� ����� ��� ȣ��
void Edge::timeOver() {
	vector<Connection*>().swap(this->connectedList);
	this->dataQueue = 0;
	this->isOvered = false;
}