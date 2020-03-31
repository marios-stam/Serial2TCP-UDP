import socket,sys,time
from SerialPort import SerialPort
from pinging.client import getServerIP
#from com0com.com0comAPI import virtualCOMPorts 
SERVER_NAME='DESKTOP-TDO0FFA'
PORT_NUMBER=1234
CHUNK_SIZE=20

#Searching and connecting to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address=getServerIP()#socket.gethostbyname(SERVER_NAME)#'192.168.2.11' 
print('Server IP:'+address)
s.connect((address, PORT_NUMBER))
print('Connected !!!')

full_msg = ''
msg=bytes(1)

#Configuring variables for speed calculations
start=time.clock()
length=0

#Managind Serial Ports 
SerialPort.scanPorts()
COMport='COM6'#virtualCOMPorts[-1]#The COM Port which is paired with the TELEMETRY GUI PORT (virtualCOMPorts id from com0com.py)
serialPort=SerialPort(COMport)

while True:
    #diff=time.clock()-start
    msg = s.recv(CHUNK_SIZE)
    serialPort.write(msg)#TODO: check if size of msg doesn lag the process
    #length+=sys.getsizeof(msg)#get bytes of msg receieved
    """ 
    if (diff>1):
        print(length/1000,'ΚBps')
        length=0
        start=time.clock()
    """