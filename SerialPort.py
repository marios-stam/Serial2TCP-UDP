import serial
import serial.tools.list_ports as port_list

class SerialPort ():
    def __init__ (self, portName,BaudRate,File,clientsList):
        self.portName = portName
        self.baudrate=BaudRate
        self.File=File
        self.CLIENTS=clientsList
        self.shouldRun=True
        try:
            self.ser=self.connectPort()
        except Exception as e:
            print(f"Erronr connecting with port {self.portName}")
            print(e)
            self.shouldRun=False

    def run(self):
        if (self.shouldRun==False):
            print('Stopping Serial thread')
            raise SystemExit()     
        print('Started Serial thread')
    
    def connectPort(self):
        ser = serial.Serial(self.portName, self.baudrate)
        print ('Connected with ',ser.name)
        return ser
    
    def listen(self):
        while True:
            try:
                data=(self.ser.read(100))
            except:
                print('COM port disconnected..Closing file')
                self.File.close()
                break
             
            self.File.write(data)
            for i in self.CLIENTS:
                try:
                    i.sendData()
                except Exception as e:
                    print(f"Client{i.clientAddress} disconnected")
                    print(e)
                    self.CLIENTS.remove(i)    
    
    @staticmethod
    def portsScan():
        print('Searching for Serial ports:')
        ports = list(port_list.comports())
        if len(ports)==0:
            print('-None Serial Port Found')
            return 
        for p in ports:
            print ('\t-',p)

