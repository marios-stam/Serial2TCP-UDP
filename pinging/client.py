
import socket
import os

def cls():#clears the console
    os.system('cls' if os.name=='nt' else 'clear')

bytesToSend= str.encode("Hello UDP Server")
bufferSize = 1024
ACK_MESSAGE='THIS IS SERIAL2TCP/UDP SERVER'

 
def getServerIP():
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.settimeout(0.15)

 
    for i in ['127.0.0.1']+list(range(0,256)):
        try:
            IP="192.168.2."+str(i) if i!='127.0.0.1' else i 
            print(IP,end=" ") 
            UDPClientSocket.sendto(bytesToSend, (IP, 20001))
            msg,IP = UDPClientSocket.recvfrom(bufferSize)
            if (msg==str.encode(ACK_MESSAGE)):
                print()#printed IP wont clear without this command
                cls()
                return IP[0]
        except Exception as e:
            print(e)
    
    return 0 
    
if(__name__=='__main__'):
    IP=getServerIP()
    print('Found Server at IP:'+IP)
