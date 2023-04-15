
import socket
import json
import pickle

host='127.0.0.1'

port=1213


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

s.bind((host,port))

s.listen(5)

print('Server start at: %s:%s'%(host,port))
print("wait for connection....")

conn,addr=s.accept()

indata=conn.recv(1024)

if len(indata)==0:
	conn.close()
	print("client closed connection.")


print("rec :"+pickle.loads(indata))


outdata='echo'+indata.decode()
conn.send(outdata.encode())


