import serial
import serial.tools.list_ports as port_list
import socket
import threading
import time,sys
from WriteFile import FileManipulator
def SerialPortsScan():
    print('Searching for Serial ports:')
    ports = list(port_list.comports())
    if len(ports)==0:
        print('-None Serial Port Found')
        return 
    for p in ports:
        print ('\t-',p)


class SerialPort ():
    def __init__(self, portName,BaudRate=9600):
        self.portName = portName
        self.baudrate=BaudRate
        self.shouldRun=True
        try:
            self.ser=self.connectPort()
        except Exception as e:
            print(f"Erronr connecting with port {self.portName}")
            print(e)
            self.shouldRun=False

    def run(self):
        if (self.shouldRun==False):
            print('Stopping Serial thread')
            raise SystemExit()     
        print('Started Serial thread')
    
    def connectPort(self):
        ser = serial.Serial(self.portName, self.baudrate)
        print ('Connected with ',ser.name)
        return ser
    
    def listen(self):
        global data,CLIENTS
        while True:
            try:
                data=(self.ser.read(100))
            except:
                print('COM port disconnected..Closing file')
                File.close()
                break
             
            File.write(data)
            for i in CLIENTS:
                try:
                    i.sendData()
                except Exception as e:
                    print(f"Client{i.clientAddress} disconnected")
                    print(e)
                    CLIENTS.remove(i)    
        

class ThreadedServer(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.shouldRun=True
    def run(self):
        self.listen()
        
    def listen(self):
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

    def sendData(self):
        self.csocket.send(data)
                    
            
        
data=bytes("Hi, This is from Server...",'utf-8')
CLIENTS=[]

if __name__ == "__main__":
    
    PORT_NUMBER = 666
    BAUD_RATE=115200    
    server=ThreadedServer('',PORT_NUMBER)
    server.daemon=True #stops when main programm ends
    server.start()
    
    File=FileManipulator('TelemetryData.tlmdt')
    File.write(data)
   
    SerialPortsScan()
    print('Starting Serial thread')
    serialPort=SerialPort('COM4',BAUD_RATE)
    serialPort.listen()
    print('Telos!!!')
    input('Press enter to terminate...')
    