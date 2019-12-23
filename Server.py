import threading
import socket
import Node
import Edge
import Preference

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

        if recv_data == "start":
            # initialize
            print('start received : ' , sender[0], sender[1], "from edge")
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

def socket_iot():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    recv_addr = ('0.0.0.0', 8889)
    sock.bind(recv_addr)

    while True:
        data_size = 256
        data, sender = sock.recvfrom(data_size)

        recv_data = data.decode()
        if recv_data == "start":
            print('start received : ' , sender[0], 'from iot')
            for node in nodeList:
                if node.IP == sender[0]:
                    node.setReady = True
                    node.sendAck(sender)
        else:
            split_data = recv_data.split(',')
            if split_data[0] == "queuesize":
                # receive using queue size for scheduling
                size = int(split_data[1])
                for node in nodeList:
                    if node.IP == sender[0]:
                        node.setData(size)


def init():
    for edge in edgeNameList:
        edge__ = Edge.Edge(edge)
        #edge__.setReady(True)
        edgeList.append(edge__)
        
    
    for node in nodeNameList:
        node__= Node.Node(node)
        #node__.setReady(True)
        nodeList.append(node__)

    edgeList[0].setIP("192.168.0.2")
    edgeList[1].setIP("192.168.0.3")
    edgeList[2].setIP("192.168.0.5")
    edgeList[3].setIP("192.168.0.6")
    edgeList[4].setIP("192.168.0.11")

    nodeList[0].setIP('')
    nodeList[0].setMAC('')

    nodeList[1].setIP('')
    nodeList[1].setMAC('')

    nodeList[2].setIP('')
    nodeList[2].setMAC('')

    nodeList[3].setIP('')
    nodeList[3].setMAC('')

    nodeList[4].setIP('')
    nodeList[4].setMAC('')
    
    nodeList[5].setIP('')
    nodeList[5].setMAC('')

    nodeList[6].setIP('')
    nodeList[6].setMAC('')

    nodeList[7].setIP('')
    nodeList[7].setMAC('')

    nodeList[8].setIP('')
    nodeList[8].setMAC('')

    nodeList[9].setIP('')
    nodeList[9].setMAC('')

    nodeList[10].setIP('')
    nodeList[10].setMAC('')

    nodeList[11].setIP('')
    nodeList[11].setMAC('')

    nodeList[12].setIP('')
    nodeList[12].setMAC('')

    nodeList[13].setIP('')
    nodeList[13].setMAC('')

    nodeList[14].setIP('')
    nodeList[14].setMAC('')

def scheduling():
    for node in nodeList:
        node.setData(10.0)
    
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
            print(conn.node.name)
    
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
        sock_edge.sendto(data.encode(), (edge.IP, edge.PORT))

    for node in nodeList:
        data = ''
        data += node.connectedEdge.name
        if node.connectType == 0:
            data += '_none'
        elif node.connectType == 1:
            data += '_ble'
        elif node.connectType == 2:
            data += '_wifi'
        sock_iot.sendto(data.encode(), (node.IP, node.PORT))

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
    #checkThread = threading.Thread(target=checkIsTrue, args=())

    socket_edge_thread.start()
    socket_iot_thread.start()
    #checkThread.start()

    scheduling_start = checkIsTrue()

    if scheduling_start == True:
        scheduling()

__main__()