import socket
PING_PORT   = 20001
bufferSize  = 1024
msgFromServer= str.encode('THIS IS SERIAL2TCP/UDP SERVER')

import threading
class ThreadedPingServer(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def run(self):
        self.listen()
        
    def listen(self):
        print("UDP server up and listening")
        # Listen for incoming datagrams
        while(True):
            message,address = self.sock.recvfrom(bufferSize)
            print('-Ping Server:New approach->'+address[0])
            # Sending a reply to client
            self.sock.sendto(msgFromServer, address)

if(__name__=='__main__'):
    server=ThreadedPingServer("0.0.0.0",PING_PORT)
    server.daemon=True #stops when main programm ends
    server.start()
    