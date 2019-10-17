#pragma once
class Node;
class Connection
{
public:
	Node* node;
	int connectionType;

public:
	Connection(Node* node, int connectionType);
};

