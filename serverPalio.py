import serial
import serial.tools.list_ports as port_list
import socket
import threading
import time

def SerialPortsScan():
    print('Searching for Serial ports:')
    ports = list(port_list.comports())
    if len(ports)==0:
        print('-None Serial Port Found')
        return 
    for p in ports:
        print ('\t-',p)
def ConnectPort(name,baudrate=9600):
    ser = serial.Serial(name, baudrate)
    print ('Connected with ',ser.name)
    return ser

class ReadingSerialPort (threading.Thread):
    def __init__(self, portName):
        threading.Thread.__init__(self)
        self.portName = portName
        self.shouldRun=True
        try:
            self.ser=ConnectPort(self.portName,baudrate=9600)
        except Exception as e:
            print(f"Erronr connecting with port {self.portName}")
            print(e)
            self.shouldRun=False
            

    def run(self):
        if (self.shouldRun==False):
            print('Stopping Serial thread')
            raise SystemExit()
        
        print('Started Serial thread')
        global data
        while True:
            data=(self.ser.readline())
            #print (data)

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            print(f'Conection from {address}')
            threading.Thread(target = self.sendToClient,args = (client,address)).start()          
            

    def sendToClient(self, client, address):
        while True:
            time.sleep(0.1)
            client.send(bytes(str(data),"utf-8"))

data=""

if __name__ == "__main__":
    SerialPortsScan()
    print('Starting Serial thread')
    serialThread=ReadingSerialPort('COM4')
    serialThread.start()
    

    while True:
        port_num = input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    ThreadedServer('',port_num).listen()
