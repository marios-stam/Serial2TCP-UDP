
import socket

bytesToSend= str.encode("Hello UDP Server")
bufferSize = 1024
ACK_MESSAGE='THIS IS SERIAL2TCP/UDP SERVER'

 
def getServerIP():
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.settimeout(0.5)

 
    for i in ['127.0.0.1']+list(range(0,256)):
        try:
            IP="192.168.2."+str(i) if i!='127.0.0.1' else i 
            #print(IP) 
            UDPClientSocket.sendto(bytesToSend, (IP, 20001))
            msg,IP = UDPClientSocket.recvfrom(bufferSize)
            if (msg==str.encode(ACK_MESSAGE)):
                return IP[0]
        except Exception as e:
            print(e)
    
    return 0 
    
if(__name__=='__main__'):
    IP=getServerIP()
    print('Found Server at IP:'+IP)
