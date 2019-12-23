import socket
import Preference
import Edge
class Node:
    def __init__(self, node_name):
        self.name = node_name

        self.dataQueue = 0.0 # IoT node에 남아있는 Queue 정보
        self.processSize = 0.0 # 이번 Timeslot 에 보낼 size

        self.connectType = 0
        self.connectedPreference = 0.0

        self.preferenceList = []

        self.isConnected = False
        self.isReady = False

        self.connectedEdge = None
    
    def setIP(self, IP):
        self.IP = IP

    def setMAC(self, MAC):
        self.MAC = MAC
    
    def setReady(self, ready=False):
        self.isReady = ready    
    
    def setData(self, inputSize):
        self.dataQueue = inputSize
    
    def sendAck(self, sender):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto("ack".encode(), sender)
        sock.close()
    
    def sendScheduleResult(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto("ack".encode(), ('', ''))
        sock.close()

    def getProcessSize(self):
        if self.connectType == 0:
            self.processSize = 0.0

        elif self.connectType == 1:
            # BLE
            if self.dataQueue > 0.6:
                a = self.dataQueue / 0.6
                b = self.dataQueue % 0.6
                if a > 2:
                    self.processSize = 1.2
                else:
                    if b > 0.45:
                        self.processSize = 0.6 + b
                    else :
                        self.processSize = 0.6
            else:
                if self.dataQueue > 0.45:
                    self.processSize = self.dataQueue
                else:
                    self.processSize = 0.0
        elif self.connectType == 2:
            if self.dataQueue > 30.0:
                self.processSize = 30.0
            else:
                self.processSize = self.dataQueue

    def addPreferenceList(self, preference):
        self.preferenceList.append(preference)
    
    def connectMostPreferEdge(self):
        if len(self.preferenceList) == 0:
            self.isConnected = True
            self.connectedEdge = Edge.Edge('')
            self.connectType = 0
            self.connectedPreference = 0
        else:
            __min = 10000000.0
            idx = -1
            prefer = 0.0
            count = 0
            for preference in self.preferenceList:
                prefer = preference.preference
                if prefer < __min:
                    __min = prefer
                    idx = count

                count += 1
            
            self.connectedEdge = self.preferenceList[idx].edge
            self.connectType = self.preferenceList[idx].type
            self.connectedPreference = self.preferenceList[idx].preference
            self.connectedEdge.newConnect(self, self.connectType)
            self.isConnected = True

    def disConnected(self):
        #self.preferenceList.remove(self.connectedEdge)
        for prefer in self.preferenceList:
            if prefer.edge == self.connectedEdge:
                self.preferenceList.remove(prefer)
                break
            
        self.connectedEdge = Edge.Edge('')
        self.connectType = 0
        self.connectedPreference = 0.0
        self.isConnected = False
    
    def timeOver(self):
        self.processSize()
        self.preferenceList.clear()
        self.isConnected = False
        self.connectType =0
        self.connectedPreference =0.0
        self.connectedEdge = Edge.Edge('')