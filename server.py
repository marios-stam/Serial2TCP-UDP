import socket
import threading
import time,sys
from FileCommands import FileManipulator
from SerialPort import SerialPort



class ThreadedServer(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.shouldRun=True
        self.IP=socket.gethostbyname(socket.gethostname())

    def run(self):
        self.listen()
        
    def listen(self):
        print('Server is listening in',self.IP,':',self.port )
        self.sock.listen(5)
        while self.shouldRun:
            client, address = self.sock.accept()
            client.settimeout(60)
            print(f'Conection from {address}')
            CLIENTS.append( ClientThread(client,address) )
            CLIENTS[-1].daemon=True #stops when main programm ends
            CLIENTS[-1].start()

    def kill(self):
        self.shouldRun=False
    

class ClientThread(threading.Thread):
    def __init__(self,clientsocket,clientAddress):
        threading.Thread.__init__(self)
        self.clientAddress=clientAddress
        self.csocket = clientsocket
        print ("New Client added: ", clientAddress)

    def run(self):
        self.csocket.send(data)

    def sendData(self,data):
        self.csocket.send(data)
                    
data=bytes("Hi, This is from Server...",'utf-8')
            
if __name__ == "__main__":
    
    CLIENTS=[]

    PORT_NUMBER = 1234
    BAUD_RATE=115200   

    server=ThreadedServer('0.0.0.0',PORT_NUMBER)
    server.daemon=True #stops when main programm ends
    server.start()
    
    File=FileManipulator('TelemetryData.tlmdt')
    File.write(data)

    
    SerialPort.portsScan()
    
    COMport=input('Enter the  COM port which is going to be shared(COMx):')
    #print('Starting Serial thread')
    serialPort=SerialPort(COMport,BAUD_RATE,File,CLIENTS)
    serialPort.listen()
    print('Telos!!!')
    input('Press enter to terminate...')