"""import serial

ser=serial.Serial('COM4',115200)

while True:
    print(ser.inWaiting())
    print(ser.out_waiting)
    input('press to reset')
    ser.flushInput()
    ser.flushOutput()
    input('press to print')"""
import subprocess,time
import psutil,os,signal

def kill(programm):
    for pid in (process.pid for process in psutil.process_iter() if process.name()==programm):
        os.kill(pid,signal.SIGTERM)
    

cmd=r'C:\Users\mario\Desktop\MARIOS\FORMULA\Telemetry\TelemetryTester\"UoP Telemetry GUI".exe'
process = subprocess.Popen(cmd,shell=True)

"""time.sleep(2)#wait 2 secs to load the GUI
kill(r'UoP Telemetry GUI.exe')"""


