#include "Node.h"
#include "Edge.h"
#include "Preference.h"
#include <random>
#include <iostream>

using namespace std;

Node::Node(double x, double y, int no, bool isCam) {
	this->no = no;
	this->x = x;
	this->y = y;
	this->isCam = isCam;

	dataQueue = 0.0;
	connectType = 0;
	connectedPreference = 0.0;
	isConnected = false;

	this->setInputSize(0);
}

/*
	�����ð����� ����Ǵ� �� ������
	1 : 100Kbit, �ִ� 10000Kbit(10Mbit)������ ���� ����
	�ܼ� ���������ʹ� �ִ� 2.5����, �̹��� �����ʹ� �ִ� 55���� ����
*/
void Node::setInputSize(int size) {
	this->inputSize = (double)size / 10.0;
	cout << this->inputSize << endl;
	if (this->inputSize > 2.0) {
		if (this->isCam) {
			if (this->inputSize > 3.0) {
				this->inputSize = 3.0;
			}
			this->inputSize *= 10;
			//this->inputSize += 20;
		}
		else {
			this->inputSize = 2.5;
		}
	}
}

/*
	�����ð����� �۽ŷ�
	BLE : �ִ� 128Kbps, 1.28���� ó������
	WIFI : static, 6Mbps, 60ó��
*/
void Node::setProcessSize() {
	switch (this->connectType) {
	case 0:
		// non connection
		this->processSize = 0.0;
		break;
	case 1:
		// BLE
		this->processSize = this->dataQueue;
		if (this->processSize >= 1.28)
			this->processSize = 1.28;
		break;
	case 2:
		// WIFI
		this->processSize = 60.0;
		break;
	}
}

/*
	���ο� Time slot�� ������ data�� Queue�� ����
	�� �Լ��� ȣ��Ǳ� ���� setInputSize�� ���� ���ο� Time slot�� ������ �������� �ѷ��� �˾ƾ� �Ѵ�. 
*/
void Node::generateData() {
	this->dataQueue += this->inputSize;
	this->checkOver();
}

/*
	�� Time slot�� ����Ǹ� ������ ������ ó������ ������ش�.
*/
void Node::processData() {
	this->dataQueue -= this->processSize;
	if (dataQueue < 0)
		dataQueue = 0.0;
}

// ��ȣ���� ��� �� ����Ʈ�� �߰�
void Node::addPreferenceList(Preference* preference) {
	this->preferenceList.push_back(preference);
}

// ������ ��ȣ�� ����Ʈ �� ���� ��ȣ���� ���� Edge�� ������ ����
// ���� �������� ��ȣ���� ����.
void Node::connectMostPreferEdge() {
	if (this->preferenceList.size() == 0) {
		this->isConnected = true;
		this->connectedEdge = nullptr;
		this->connectType = 0;
		this->connectedPreference = 0;
	}
	else {
		double min = DBL_MAX;
		int index = -1;
		double preference;
		for (size_t i = 0; i < this->preferenceList.size(); i++) {
			preference = this->preferenceList[i]->preference;
			if (preference < min) {
				min = preference;
				index = i;
			}
		}
		this->connectedEdge = this->preferenceList[index]->edge;
		this->connectType = this->preferenceList[index]->type;
		this->connectedPreference = this->preferenceList[index]->preference;
		this->connectedEdge->newConnect(this, connectType);
		this->isConnected = true;
	}
}

// Edge�� ���� ������ �������� ��� ȣ���
void Node::disConnected() {
	for (size_t i = 0; i < this->preferenceList.size(); i++) {
		if (this->preferenceList[i]->edge == this->connectedEdge)
			this->preferenceList.erase(this->preferenceList.begin() + i);
	}
	this->connectedEdge = nullptr;
	this->connectType = 0;
	this->connectedPreference = 0;
	this->isConnected = false;
}

// ����� Data Queue�� �ʰ��Ǿ����� üũ, �������
void Node::checkOver() {
	if (this->dataQueue > 100)
		cout << "Error : Node�� data overflow �߻�, " << this->no << endl;
}

// �� Time slot�� ����� ��� ȣ��Ǵ� �Լ�
void Node::timeOver() {
	this->processData();
	vector<Preference*>().swap(this->preferenceList);
	this->isConnected = false;
	this->connectType = 0;
	this->connectedPreference = 0;
	this->connectedEdge = nullptr;
}