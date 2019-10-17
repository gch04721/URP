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
	단위시간동안 생산되는 총 데이터
	1 : 100Kbit, 최대 10000Kbit(10Mbit)데이터 저장 가능
	단순 센서데이터는 최대 2.5까지, 이미지 데이터는 최대 55까지 생성
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
	단위시간동안 송신량
	BLE : 최대 128Kbps, 1.28까지 처리가능
	WIFI : static, 6Mbps, 60처리
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
	새로운 Time slot에 생성된 data를 Queue에 저장
	이 함수가 호출되기 전에 setInputSize를 통해 새로운 Time slot에 생성된 데이터의 총량을 알아야 한다. 
*/
void Node::generateData() {
	this->dataQueue += this->inputSize;
	this->checkOver();
}

/*
	한 Time slot이 종료되면 전송한 데이터 처리량을 계산해준다.
*/
void Node::processData() {
	this->dataQueue -= this->processSize;
	if (dataQueue < 0)
		dataQueue = 0.0;
}

// 선호도를 계산 후 리스트에 추가
void Node::addPreferenceList(Preference* preference) {
	this->preferenceList.push_back(preference);
}

// 본인의 선호도 리스트 중 가장 선호도가 높은 Edge에 연결을 진행
// 값이 낮을수록 선호도가 높음.
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

// Edge에 의해 연결이 끊어지는 경우 호출됨
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

// 노드의 Data Queue가 초과되었는지 체크, 출력해줌
void Node::checkOver() {
	if (this->dataQueue > 100)
		cout << "Error : Node의 data overflow 발생, " << this->no << endl;
}

// 한 Time slot이 종료된 경우 호출되는 함수
void Node::timeOver() {
	this->processData();
	vector<Preference*>().swap(this->preferenceList);
	this->isConnected = false;
	this->connectType = 0;
	this->connectedPreference = 0;
	this->connectedEdge = nullptr;
}