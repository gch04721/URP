#pragma once
#include <vector>
#include <random>

class Edge;
class Preference;

class Node
{
public:
	int no; // node number
	double x, y; // position

	double dataQueue; // max 100, 1 : 100Kbit
	double inputSize; // 1 : 100Kbit
	double processSize; // 1: 100Kbit

	Edge* connectedEdge;
	int connectType;
	bool isConnected;
	double connectedPreference;

	bool isCam;

	std::vector<Preference*> preferenceList;

public:
	Node(double x, double y, int no, bool isCam);
	void setInputSize(int size);
	void setProcessSize();
	void generateData();
	void processData();

	void addPreferenceList(Preference* preference);
	void connectMostPreferEdge();
	void disConnected();
	void checkOver();
	void timeOver();
};

