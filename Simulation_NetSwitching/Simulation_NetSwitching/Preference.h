#pragma once
class Node;
class Edge;

class Preference
{
public:
	Node* node;
	Edge* edge;
	double preference;
	int type;

public:
	Preference(Node* node, Edge* edge, bool checkBLE);
	double getPreference(bool checkBLE);
};

