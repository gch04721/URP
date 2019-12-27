import threading
import sys
import socket

Mac_List={'node1' : 'B8:27:EB:25:06:42', 'node2' : 'B8:27:EB:5E:F7:42'\
         ,'node3' : 'B8:27:EB:7C:87:60', 'node4' : 'B8:27:EB:9D:BF:80'\
         ,'node5' : 'B8:27:EB:B8:7E:66', 'node6' : 'B8:27:EB:C3:75:5C'\
         ,'node7' : 'B8:27:EB:6D:FE:49', 'node8' : 'B8:27:EB:5A:58:F7'}
count = 0
ble_connected = False

def sendToMain(sendStr):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(sendStr.encode(), ('192.168.0.8', 8888))
    s.close()

def server_iot():
    global count

    sock_iot = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_iot.bind(('0.0.0.0',8890))

    while True:
        print('Waiting data from IoT')
        data,addr = sock_iot.recvfrom(3000000)
        print('Server is received data:',data.decode())
        print('Send IoT IP :', addr[0])
        print('Send Iot Port:', addr[1])
        if 'send1' == data.decode():
            count = count - 1
            if count == 0 :
                sendToMain('end')


def server_main():
    global count
    sock_main = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_main.bind(('0.0.0.0',8888))
    while True:
        print('Waiting data from Server')
        data,addr = sock_main.recvfrom(200)
        recv_data = data.decode()
        print('server is received data:', data.decode())
        print('send Main IP :', addr[0])
        print('send Main port :', addr[1])
        if recv_data != "" : 
            recv_data = recv_data.split(',')
            count = len(recv_data)
            print(count)
            threading.Thread(target = bluetooth, args=())

def bluetooth():
    global count
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.bind(('B8:27:EB:C3:75:5C', 1))
    while True:
        s.listen(1)
        client, address = s.accept()
        print(client, address)
        recv_data = client.recv(1024)
        
        if recv_data.decode() == 'send0':
            print(recv_data)
        elif recv_data.decode() == 'send1':
            count -= 1
            client.close()

        if count == 0:
            s.close()
            sendToMain('end')
            break


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto('start'.encode(), ('192.168.0.8', 8888))
    data,addr = sock.recvfrom(200)

    recv_data = data.decode()
    
    if recv_data == "ack":
        print("Main Server established")

        my_thread = threading.Thread(target=server_iot, args=())
        my_thread.start()  
        my_thread = threading.Thread(target=server_main, args=())
        my_thread.start()
        sock.close()
