import threading
import socket
import Node
import Edge
import Preference
from time import sleep
time_limit = 5
current_time = 0

edgeNameList = ('edge1', 'edge2', 'edge3', 'edge4', 'edge5')
edgeList=[]

nodeNameList = ('node1', 'node2', 'node3', 'node4', 'node5', 'node6', 'node7', 'node8', \
            'node9', 'node10', 'node11', 'node12', 'node13', 'node14', 'node15')
nodeList=[]

scheduling_start = False

def socket_edge():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    recv_addr = ('0.0.0.0', 8888)
    sock.bind(recv_addr)

    while True:
        data_size = 256
        data, sender = sock.recvfrom(data_size)

        recv_data = data.decode()
        print('data received : ' , sender[0], sender[1], "from edge", ": ", recv_data)
        if recv_data == "start":
            # initialize
            
            for edge in edgeList:
                if edge.IP == sender[0]:
                    edge.setReady(True)
                    edge.sendAck(sender)

        else:
            if recv_data == "end":
                # Edge server receive end
                for edge in edgeList:
                    if edge.IP == sender[0]:
                        edge.setReady(True)
                        for conn in edge.connectedList:
                            conn.node.setReady(False)
                            conn.node.timeOver()
                        edge.timeOver()

def socket_iot():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    recv_addr = ('0.0.0.0', 8889)
    sock.bind(recv_addr)

    while True:
        data_size = 512
        data, sender = sock.recvfrom(data_size)
        print(data)
        print(sender)
        recv_data = data.decode()
        if recv_data == "start":
            print('start received : ' , sender[0], 'from iot')
            for node in nodeList:
                if node.IP == sender[0]:
                    node.setReady(True)
                    node.sendAck(sender)
        else:
            print(recv_data)
            split_data = recv_data.split(',')
            print(split_data)
            if split_data[0] == "queue_info":
                # receive using queue size for scheduling
                size = float(split_data[1])
                for node in nodeList:
                    if node.IP == sender[0]:
                        node.setData(size)
                        node.setReady(True)
                        node.sendAck(sender)
                        print(size)


def init():
    for edge in edgeNameList:
        edge__ = Edge.Edge(edge)
        #edge__.setReady(True)
        edge__.setReady(False)
        edgeList.append(edge__)
    
    for node in nodeNameList:
        node__= Node.Node(node)
        node__.setReady(True)
        #node__.setReady(False)
        nodeList.append(node__)

    edgeList[0].setIP("192.168.0.2")
    edgeList[1].setIP("192.168.0.3")
    edgeList[2].setIP("192.168.0.5")
    edgeList[3].setIP("192.168.0.6")
    edgeList[4].setIP("192.168.0.11")

    # arduino : 10
    nodeList[0].setIP('192.168.0.10')
    nodeList[0].setMAC('24:6F:28:25:23:26')

    nodeList[1].setIP('192.168.0.15')
    nodeList[1].setMAC('24:6F:28:25:22:36')

    nodeList[2].setIP('192.168.0.14')
    nodeList[2].setMAC('24:6F:28:25:22:8A')

    nodeList[3].setIP('192.168.0.17')
    nodeList[3].setMAC('24:6F:28:25:22:2E')

    nodeList[4].setIP('192.168.0.18')
    nodeList[4].setMAC('24:6F:28:25:21:72')
    
    nodeList[5].setIP('192.168.0.19')
    nodeList[5].setMAC('24:6F:28:25:21:CE')

    nodeList[6].setIP('192.168.0.20')
    nodeList[6].setMAC('24:6F:28:25:22:4A')

    nodeList[7].setIP('192.168.0.21')
    nodeList[7].setMAC('24:6F:28:25:22:02')

    nodeList[8].setIP('192.168.0.22')
    nodeList[8].setMAC('24:6F:28:25:22:92')

    nodeList[9].setIP('192.168.0.23')
    nodeList[9].setMAC('24:6F:28:25:21:C6')

    # pi zero w: 5
    nodeList[10].setIP('192.168.0.9')
    nodeList[10].setMAC('B8:27:EB:25:06:42')

    nodeList[11].setIP('192.168.0.12')
    nodeList[11].setMAC('B8:27:EB:5E:F7:42')

    nodeList[12].setIP('192.168.0.13')
    nodeList[12].setMAC('B8:27:EB:7C:87:60')

    nodeList[13].setIP('192.168.0.4')
    nodeList[13].setMAC('B8:27:EB:9D:BF:80')

    nodeList[14].setIP('192.168.0.7')
    nodeList[14].setMAC('B8:27:EB:B8:7E:66')

def getData():
    while True:
        count = 0
        for node in nodeList:
            if node.name in ('node11', 'node12', 'node13', 'node14', 'node15'):
                if node.getData == False:
                    node.sendQueueInfo()
                    
                else:
                    count += 1

        if count == 5:
            break
        else:
            sleep(5)



def scheduling():
    # for test
    
    checkIsTrue()

    getData()
    # for node in nodeList:
    #     node.setData(10.0)
    # nodeList[4].setData(49)

    for node in nodeList:
        for edge in edgeList:
            checkBLE = True
            pr = Preference.Preference(node, edge, checkBLE)
            node.addPreferenceList(pr)

    for node in nodeList:
        node.connectMostPreferEdge()

    for edge in edgeList:
        edge.stabilizeQueue()
    
    while isFinished() == False:
        for node in nodeList:
            if(node.isConnected == False):
                node.connectMostPreferEdge()
                if node.connectType != 0:
                    node.connectedEdge.stabilizeQueue()

    for edge in edgeList:
        print(edge.name , "의 연결 노드 :")
        for conn in edge.connectedList:
            print(conn.node.name,',', conn.node.connectType)
    
    sock_edge = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_iot = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for edge in edgeList:
        data = ''
        for conn in edge.connectedList:
            data += conn.node.name
            if conn.node.connectType == 0:
                data += '_none'
            elif conn.node.connectType == 1:
                data += '_ble'
            elif conn.node.connectType == 2:
                data += '_wifi'
            data += ','
        data = data[:-1]
        print(data)
        sock_edge.sendto(data.encode(), (edge.IP, edge.PORT))
        edge.setReady(False)
    

    for node in nodeList:
        data = ''
        data += node.connectedEdge.name
        if node.connectType == 0:
            data += '_none'

        elif node.connectType == 1:
            data += '_ble'
            data += ','
            data += str(node.processSize)
            data += ','
            if node.processSize > 0.6:
                data += '2'
            else:
                data += '1'

        elif node.connectType == 2:
            data += '_wifi'
            data += ','
            data += str(node.processSize)
        
        sock_iot.sendto(data.encode(), (node.IP, node.PORT))
        node.setReady(False)
        node.getData = False

    threading.Timer(5 * 60, scheduling)

def isFinished():
    for node in nodeList:
        if node.isConnected == False:
            return False
    return True

def checkIsTrue():
    while True:
        check = True
        for edge in edgeList:
            if edge.isReady == False:
                check = False
        
        for node in nodeList:
            if node.isReady == False:
                check = False

        if check ==True :
            return True
                
    

def __main__():
    init()
    socket_edge_thread = threading.Thread(target=socket_edge, args= ())
    socket_iot_thread = threading.Thread(target= socket_iot, args= ())

    socket_edge_thread.start()
    socket_iot_thread.start()

    scheduling()

__main__()