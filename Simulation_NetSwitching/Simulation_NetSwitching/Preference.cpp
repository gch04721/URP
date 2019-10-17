#include "Preference.h"
#include "Node.h"
#include "Edge.h"
#include <cmath>

Preference::Preference(Node* node, Edge* edge, bool checkBLE) {
	this->node = node;
	this->edge = edge;
	this->preference = this->getPreference(checkBLE);
}

double Preference::getPreference(bool checkBLE) {
	double min = DBL_MIN;

	this->node->connectType = 2;
	this->node->setProcessSize();
	double p_wifi = 210.0;
	double q_wifi = this->node->dataQueue - this->node->processSize;
	if (q_wifi < 0.0)
		q_wifi = 0.0;

	double v = 3.8;
	min = p_wifi + v * q_wifi;
	this->type = 2;

	if (checkBLE) {
		this->node->connectType = 1;
		this->node->setProcessSize();
		double p_ble = 0.0076 * log(this->node->processSize * 100) + 0.01;
		double q_ble = this->node->dataQueue - this->node->processSize;
		if (q_ble < 0.0)
			q_ble = 0.0;
		double min_ble = p_ble + v * q_ble;

		if (min_ble < min) {
			min = min_ble;
			this->type = 1;
		}
	}
	this->node->connectType = 0;
	this->node->setProcessSize();

	return min;
}