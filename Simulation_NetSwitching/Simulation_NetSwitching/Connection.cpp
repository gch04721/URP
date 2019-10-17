#include "Connection.h"
#include "Node.h"

Connection::Connection(Node* node, int connectionType) {
	this->node = node;
	this->connectionType = connectionType;
}