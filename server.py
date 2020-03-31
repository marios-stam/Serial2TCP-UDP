import socket
import threading
import time,sys
from FileCommands import FileManipulator
from SerialPort import SerialPort
from pinging.server import ThreadedPingServer,PING_PORT


class ThreadedServer(threading.Thread):
    """The thread of the main server.It listens for new connections from clients 
        and then it establishes them.
        Attributes: 
        	host  (str): The IP of the host. 
            port  (int): The TCP port number.       
    """
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creates socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))#binds it to the appropritae address and port
        self.shouldRun=True
        self.IP=socket.gethostbyname(socket.gethostname())

    def run(self):
        self.listen()
        
    def listen(self):
        """In every loop it:
            -waits for a new collection from a client
            -creates a new thread for every client
            -adds it to the CLIENTS list
        """
        print('Server is listening in',self.IP,':',self.port )
        self.sock.listen(5)
        while self.shouldRun:
            client, address = self.sock.accept()#waits for a new collection from a client
            client.settimeout(60)
            #print(f'Conection from {address}')
            CLIENTS.append( ClientThread(client,address) )#creates a new thread for every client
            #                                              and adds it to the CLIENTS list                  
            CLIENTS[-1].daemon=True #stops when main programm ends
            CLIENTS[-1].start()

    def kill(self):
        self.shouldRun=False
    

class ClientThread(threading.Thread):
    """Every client is represented by this thread"""
    def __init__(self,clientsocket,clientAddress):
        threading.Thread.__init__(self)
        self.clientAddress=clientAddress
        self.csocket = clientsocket
        print ("New Client added:",clientAddress[0]+":"+str(clientAddress[1]))

    def run(self):
        self.csocket.send(data)

    def sendData(self,data):
        """Sends data to this Client
         Parameters: 
            data (Bytes): The data to be sent.
        """
        self.csocket.send(data)
                    
data=bytes("Hi, This is from Server...",'utf-8')
            
if __name__ == "__main__":
    
    CLIENTS=[]

    PORT_NUMBER = 1234
    BAUD_RATE=115200   
    
    print('-Starting Ping Server')
    Pingserver=ThreadedPingServer("0.0.0.0",PING_PORT)
    Pingserver.daemon=True #stops when main programm ends
    Pingserver.start()

    print('-Starting Main Server')
    server=ThreadedServer('0.0.0.0',PORT_NUMBER)
    server.daemon=True #stops when main programm ends
    server.start()
    
    File=FileManipulator('TelemetryData.tlmdt')
    File.write(data)

    
    desiredModule='Arduino'   
    try:
        COMport=SerialPort.findPortOf(desiredModule)#input('Enter the  COM port which is going to be shared(COMx):')
        print(desiredModule,'found at:'+COMport)
        serialPort=SerialPort(COMport,BAUD_RATE,File,CLIENTS)
        serialPort.listen()
    except Exception as e:
        print(e)
        
    
    
    print('Finished!!!')
    input('Press enter to terminate...')