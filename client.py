import socket,sys,time
from SerialPort import SerialPort

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address=input('Insert Server IP:')
#port=input('Insert port Number:')
s.connect((address, 1234))
print('Connected !!!')
full_msg = ''
msg=bytes(1)

start=time.clock()
length=0
SerialPort.portsScan()
COMport=input('insert the name of COM port where the data are going to be transmitted:')#'COM1'
serialPort=SerialPort(COMport)

while True:
    diff=time.clock()-start
    msg = s.recv(40000)
    serialPort.write(msg)#TODO: check if size of msg doesn lag the process

    length+=sys.getsizeof(msg)#get bytes of msg receieved
    
    if (diff>1):
        print(length/1000,'ΚBps')
        length=0
        start=time.clock()
        
    
