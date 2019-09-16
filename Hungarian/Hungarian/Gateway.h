#pragma once
#include <string>
#include <vector>

class Gateway
{

public:
	std::string name;
	std::vector<int> connectedDeviceList;

	double remainResource;

private:
	double totalResource;

	
};

