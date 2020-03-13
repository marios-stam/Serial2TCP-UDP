import serial
import serial.tools.list_ports as port_list
import time

ser = serial.Serial('COM4')
ser.baudrate = 230400

while True:
    s = ser.read(20000)
    for i in s:
        print(i)
    input()
    
    

    
