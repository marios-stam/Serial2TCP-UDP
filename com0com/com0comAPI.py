import os
import re
""" This file communicates with <<com0com>> software API and prints to VIRTUALCOMPORTS.cnfg
    all Virtual COM Ports and connections from this software
     
    virtualCOMPorts (list): contains  the connected Virtual COM Ports pairs
"""
#run com0com API and save output to file
os.system(r'C:\"Program Files (x86)"\com0com\setupc --output com0comAPIoutput.txt listfnames')

#open ouput file
f = open("com0comAPIoutput.txt", "r")
s=f.read()

#search COM ports in file and save them to list
virtualCOMPorts=re.findall(r'\(([^)]+)', s)
#write new file with VIRTUAL COM PORTS CONFIGURATION
f = open("VIRTUALCOMPORTS.cnfg", "w")
f.write("SERIAL2TCP/UDP:"+virtualCOMPorts[-1])
f.write('\n')
f.write("TELEMETRYGUI:"+virtualCOMPorts[0])
f.close()





    
