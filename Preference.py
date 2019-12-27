import Node
import Edge

class Preference:
    def __init__(self, node, edge, checkBLE):
        self.node = node
        self.edge = edge
        self.type = 0
        self.preference = self.getPreference(checkBLE)       

    def getPreference(self, checkBLE):
        __preference = 0.0
        self.node.connectType = 2
        self.node.getProcessSize()

        p_wifi = 270.0
        q_wifi = self.node.dataQueue *(self.node.inputSize - self.node.processSize)

        if q_wifi < 0.0:
            q_wifi = 0.0
        
        v = 0.0044
        __preference = p_wifi + v * q_wifi
        self.type = 2

        if checkBLE:
            self.node.connectType = 1
            self.node.getProcessSize()
            if 0.6 <= self.node.processSize <= 1.2:
                p_ble = 260.0
            elif self.node.processSize <= 0.6:
                p_ble = 130.0

            q_ble = self.node.dataQueue * (self.node.dataQueue - self.node.processSize)

            if q_ble < 0.0:
                q_ble = 0.0
            min_ble = p_ble + v * q_ble
            
            if min_ble < __preference:
                __preference = min_ble
                self.type = 1

        self.node.connectType = 0
        self.node.getProcessSize()
    
        return __preference