import socket,sys,time
from SerialPort import SerialPort
SERVER_NAME='DESKTOP-TDO0FFA'
PORT_NUMBER=1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address='192.168.2.11'#socket.gethostbyname(SERVER_NAME) 
print('Server IP:'+address)
s.connect((address, PORT_NUMBER))
print('Connected !!!')
full_msg = ''
msg=bytes(1)

start=time.clock()
length=0
SerialPort.scanPorts()
COMport='COM6'#The COM Port which is paired with the TELEMETRY GUI PORT
serialPort=SerialPort(COMport)

while True:
    diff=time.clock()-start
    msg = s.recv(2)
    serialPort.write(msg)#TODO: check if size of msg doesn lag the process
    length+=sys.getsizeof(msg)#get bytes of msg receieved
    
    if (diff>1):
        print(length/1000,'ΚBps')
        length=0
        start=time.clock()
        
    
