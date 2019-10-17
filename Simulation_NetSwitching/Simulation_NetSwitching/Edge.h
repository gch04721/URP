#pragma once
#include <vector>

class Node;
class Connection;
using namespace std;
class Edge
{
public:
	int no;
	double x, y; // Edge position

	double dataQueue; // max 100, 1 : 100Kbit
	bool isOvered;

	vector<Connection*> connectedList;

public:
	Edge(double x, double y, int no);
	void newConnect(Node* node, int type);
	void disConnectNode(Node* node);
	void stabilizeQueue();
	Node* leastPreferNode();
	void timeOver();
};

