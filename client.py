import socket,sys,time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#address=input('Insert Server address:')
#port=input('Insert port Number:')
s.connect(('192.168.2.3', 1234))
print('Connected !!!')
full_msg = ''
msg=bytes(1)

start=time.clock()
length=0
while True:
    diff=time.clock()-start
    msg = s.recv(20000)

    length+=sys.getsizeof(msg)#get bytes of msg receieved
    
    if (diff>1):
        print(length/1000,'ΚBps')
        length=0
        start=time.clock()
        
    
