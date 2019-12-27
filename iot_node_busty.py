import socket
import threading
import numpy as np
import time
import sys

ack_arrived = False
queue_info_arrived = False
bt_sendstart = False

queue_using = 0.0

edge_ip = {'edge1' : '192.168.0.3', 'edge2' : '192.168.0.5'}

edge_MAC = {'edge1' : 'B8:27:EB:66:C4:C9', 'edge2' : 'B8:27:EB:B5:55:88'}

def sendToMain(sendStr):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(sendStr.encode(), ('192.168.0.8', 8889))
    s.close()

def sendToEdge(edgeName, sendStr):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(sendStr.encode(), (edge_ip[edgeName], 8890))
    s.close()

def socket_main():
    global ack_arrived
    global queue_using
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', 8889))

    while True:
        data_sz = 512
        data, sender = s.recvfrom(data_sz)

        print(data, sender)
        recv_data = data.decode()
        if recv_data == 'ack':
            print('receive ack')
            ack_arrived = True

        elif recv_data == 'queue_info':
            queue_data = np.random.poisson(25, 5)
            queue_data = float(queue_data[0]) / 10.
            if queue_data > 3.3:
                    queue_data = np.random.poisson(300, 25)
                    queue_data = float(queue_data[0]) / 10.
                    if queue_data > 35.0:
                            queue_data = 35.0
            print(queue_data)
            queue_using = queue_using + queue_data
            queue_size = 'queue_info,' + str(queue_data)
            sendToMain(queue_size)

        elif 'wifi' in recv_data:
            split_data = recv_data.split(',')
            queue_using -= float(split_data[1])
            edgeName = split_data[0].split('_')[0]
            sendToEdge(edgeName,'send1')
 
        elif 'ble' in recv_data:
            socket_ble(recv_data)


def socket_ble(recv_data):
    global queue_using
    global edge_MAC
    split_data = recv_data.split(',')
    queue_using -= float(split_data[1])
    edgeName = split_data[0].split('_')[0]

    bt_s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)     
    print('wait')
    while True:
        try:
            bt_s.connect((edge_MAC[edgeName],1))
            print('connected')
            while True:
                if split_data[2] == '1':
                    bt_s.send('send1'.encode())
                    
                elif split_data[2] == '2':
                    bt_s.send('send0'.encode())
                    print('send0')
                    time.sleep(0.1)
                    bt_s.send('send1'.encode())
                    print('send1')
                    time.sleep(0.1)
                    break
        except socket.error:
                pass

    bt_s.close()


def socket_edge():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', 8890))

    while True:
        data_sz = 512
        data, sender = s.recvfrom(data_sz)

        print(data, sender)
        recv_data = data.decode()
        if recv_data == '':
            pass

def __main__():
    global ack_arrived
    
    t1 = threading.Thread(target = socket_main, args =())
    t2 = threading.Thread(target = socket_edge, args =())
    t1.start()
    t2.start()
    
    sendToMain('start')
    print('send start to main server')

__main__()
    
        
