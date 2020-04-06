import socket,sys,time,subprocess,os,psutil,signal
from SerialPort import SerialPort
from pinging.client import getServerIP
from GLOBAL_VARIABLES import TCP_READ_SIZE
import logging,time

def kill(programm):
    for pid in (process.pid for process in psutil.process_iter() if process.name()==programm):
        os.kill(pid,signal.SIGTERM)

def handler(signum, frame):
    #killing the GUI   
    kill(r'UoP Telemetry GUI.exe')
    # force quit
    sys.exit(1)  # only 0 means "ok"
    quit()

signal.signal(signal.SIGINT, handler)
#signal.signal(signal.SIGHUP, handler)
signal.signal(signal.SIGTERM,handler)

#from com0com.com0comAPI import virtualCOMPorts 
SERVER_NAME='DESKTOP-TDO0FFA'
PORT_NUMBER=1234

#executing TELEMETRY GUI
cmd=r'C:\Users\mario\Desktop\MARIOS\FORMULA\Telemetry\TelemetryTester\"UoP Telemetry GUI".exe'
process = subprocess.Popen(cmd,shell=True)

time.sleep(2)#wait 2 secs to load the GUI



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
    try:
        msg = s.recv(1024)#receiving from socket
        if len(msg)<1024:print(len(msg))
        t0=time.time()
        buffer_before_writing=serialPort.ser.out_waiting
        serialPort.write(msg)#TODO: check if size of msg doesn lag the process
        dt=(time.time()-t0)#secs
        Kbytes=len(msg)/1024
        if dt!=0:throughput=Kbytes/dt#KBps
        #print( len(msg) , dt*1000, throughput  )

    except Exception as e:
        print(e)
        kill(r'UoP Telemetry GUI.exe')
        sys.exit(1)
    
