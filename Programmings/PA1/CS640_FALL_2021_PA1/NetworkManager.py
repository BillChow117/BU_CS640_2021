import socket
from struct import unpack


#Do not modify this class. It will extract information received from the server and create necessary variables.
class NetworkManager:
    FOOD_FORMAT='2i'
    STRUCT_FORMAT='8i'

    def __init__(self) :
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def initiateConnection(self,ip,port):
        self.socket.connect((ip,port))
        return unpack('2i',self.socket.recv(8))

    def getStateInfo(self):
        incomingPacketSize=unpack('i',self.socket.recv(4))[0]
        if incomingPacketSize<0:
            return None,[]
        numAttr=(incomingPacketSize-8)/3
        data=self.socket.recv(incomingPacketSize)
        food = unpack(NetworkManager.FOOD_FORMAT,data[:8])
        lines=[]
        for i in range(8,incomingPacketSize,32):
            lines.append(unpack(NetworkManager.STRUCT_FORMAT,data[i:i+32]))
        return food,lines

    def sendCommand(self,command):
        self.socket.send(command)