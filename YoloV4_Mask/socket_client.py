import socket

import pickle

host='127.0.0.1'
port=1213

a = {'test':1, 'dict':{1:2, 3:4}, 'list': [42, 16]}
	 
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

outdata=pickle.dumps(a)
print('send:'+outdata)
s.send(outdata)

indata=s.recv(1024)
if len(indata)==0:
	s.close()
	print('server closed connection.')

print('recv :'+indata.decode())
