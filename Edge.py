import Connection
import socket
max_queue_size = 40.0
class Edge:
    def __init__(self, edge_name):
        self.name = edge_name
        self.dataQueue = 0.0
        self.PORT = 8888
        self.isOvered = False
        self.connectedList= [] # class Connection
        self.isReady = False

    def setIP(self, IP):
        self.IP = IP

    def setReady(self, ready = False):
        self.isReady = ready

    def sendAck(self, sender):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto("ack".encode(), sender)
        sock.close()

    def sendScheduleResult(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        data = str()

        sock.sendto(data.encode(), (self.IP, self.PORT))

    def stabilizeQueue(self):
        while self.isOvered:
            abandonNode = self.leastPreferNode()
            self.disConnectNode(abandonNode)
            abandonNode.disConnected()
    
    def leastPreferNode(self):
        min = 10000000.0
        leastIdx = 0
        count = 0
        for conn in self.connectedList:
            prefer = conn.node.connectedPreference
            if min > prefer:
                min = prefer
                leastIdx = count
            count += 1

        return self.connectedList[leastIdx].node
    
    def disConnectNode(self, node):
        for conn in self.connectedList:
            if conn.node == node:
                self.connectedList.remove(conn)
                break
        node.getProcessSize()
        self.dataQueue -= node.processSize

        if self.dataQueue < 0.0:
            self.dataQueue = 0.0
        if self.dataQueue > max_queue_size:
            self.isOvered = True
        else:
            self.isOvered = False

    def newConnect(self, node, type):
        self.connectedList.append(Connection.Connection(node, type))
        node.getProcessSize()
        self.dataQueue += node.processSize
        if self.dataQueue > max_queue_size: 
            self.isOvered = True
        else:
            self.isOvered = False

    def timeOver(self):
        self.connectedList.clear()
        self.dataQueue = 0.0
        self.isOvered = False
