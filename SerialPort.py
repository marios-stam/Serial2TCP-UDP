import serial
import serial.tools.list_ports as port_list

class SerialPort ():
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
        global data
        while True:
            try:
                data=(self.ser.read(20))
                #print(data)
            except:
                print('COM port disconnected..Closing file')
                self.File.close()
                break
             
            self.File.write(data)
            for i in self.CLIENTS:
                try:
                    i.sendData(data)
                except Exception as e:
                    print(f"-Client{i.clientAddress} disconnected")
                    print(e)
                    print()
                    self.CLIENTS.remove(i)#TODO: check if thread is bein killed or keep running    
    
    def write(self,data):
        self.ser.write(data)


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
        ports=SerialPort.scanPorts()
        desiredPort=None
        retry=True
        while (retry):
            for p in ports:
                if (Module in p[1]): desiredPort=p[0] #p[1] is the name and p[0] is the COM Port (p[0]='COMx')
            
            if(desiredPort==None):#if couldnt found the Module
                answer=input("Couldn't find "+Module+".......Retry (y/n)?")
                
            retry= False if (desiredPort!=None or answer.capitalize()=='N') else True

        if(desiredPort==None):
            raise Exception("Sorry.....couldn't find "+Module+"!")
        return desiredPort
        
if __name__=='__main__':
    SerialPort.scanPorts()