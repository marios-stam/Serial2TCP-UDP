import serial
import serial.tools.list_ports as port_list
from GLOBAL_VARIABLES import TCP_READ_SIZE


class SerialPort ():
    """Contains all the functions necessary for COM (serial) Port interfacing.

        Attributes: 
        	portName 	(str): The name of COM Port (e.g. ‘COM1’). 
            Baudrate  	(int): The baudrate of connection.Predefined at 115200.
	        File        (file):The file where data are going to be saved.
	        ClientList	(List of threads):Contains all the threads of clients
    """
    def __init__ (self, portName,BaudRate=115200,File=None,clientsList=None):
        # predefined as None beacause they arent needed in the client side 
        self.portName = portName
        self.baudrate=BaudRate
        self.File=File
        self.CLIENTS=clientsList
        self.shouldRun=True
        self.connectPort()
        
    def run(self):
        if (self.shouldRun==False):
            print('Stopping Serial thread')
            raise SystemExit()     
        print('Started Serial thread')
    
    def connectPort(self):
        """Conects to COM Port and saves connection to variable ser"""
        proceed=False
        while not proceed:
            try: 
                ser = serial.Serial(self.portName, self.baudrate)
                proceed=True
            except Exception as e :
                print('Couldnt connect to',self.portName)
                print(e)
                input('\tHit enter to try again....')
            

        print ('Connected with ',ser.name)
        self.ser=ser
    
    def listen(self):
        """In every loop: 
                -reads CHUNK_SIZE bytes from Serial Port
                -writes data to  file
                -sends data to every Client in the ClientList via ClientThread.sendData() method  
        """
        
        while True:

            if( len(self.CLIENTS)==0 ):
                continue


            try:
                bytesToRead = max(TCP_READ_SIZE, min(2048, self.ser.in_waiting))
                #print(bytesToRead)
                data=(self.ser.read(bytesToRead))
                #print(len(data))

            except:
                print('COM port disconnected..Closing file')
                self.File.close()
                break
             
            #self.File.write(data)#writes data to the file
            for i in self.CLIENTS:
                try:
                    i.sendData(data)
                except Exception as e:
                    print(f"-Client{i.clientAddress} disconnected")
                    print(e)
                    print()
                    self.CLIENTS.remove(i)#TODO: check if thread is bein killed or keep running    
    
    def write(self,data):
        """Writes data to Serial Port
         Parameters: 
            data (Bytes): The data to be sent.
        """
        self.ser.write(data)

    def resetBuffers(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        print("Flushed Everything")

    @staticmethod
    def scanPorts():
        print('Searching for Serial ports:')
        ports = list(port_list.comports())
        if len(ports)==0:
            print('-None Serial Port Found')
            return 
        for p in ports:
            print ('\t-',p)
        
        return ports 
        
    @staticmethod
    def findPortOf(Module):
        """Finds in which port is 'Module' connected to
         Parameters: 
             Module     (String): The name of the desired Module.
         Returns:
            desiredPort (String):The COM port name in which the module is connected
         :raises:
            'Sorry.....couldn't find Module!': if Module  is not connected to PC.

        
        """  
        desiredPort=None
        retry=True
        while (retry):
            ports=SerialPort.scanPorts()
            for p in ports:
                if (Module in p[1]): desiredPort=p[0] #p[1]-->name and p[0]-->COM Port (p[0]='COMx')
            
            if(desiredPort==None):#if couldnt found the Module
                answer=input("Couldn't find "+Module+".......Retry (y/n)?")
                
            retry= False if (desiredPort!=None or answer.capitalize()=='N') else True

        if(desiredPort==None):
            raise Exception("Sorry.....couldn't find "+Module+"!")
        return desiredPort
        
if __name__=='__main__':
    SerialPort.scanPorts()
    help(SerialPort)