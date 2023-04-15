from tkinter import *
import tkinter as tk
from tkhtmlview import HTMLLabel
import tkinter.font as tkFont
import socket
import threading
import time

host='127.0.0.1'

port=1213

outdata=""
indata=''
cal_data=['0','0','0']

root=Tk()

total_count=tk.StringVar()

y=tk.StringVar()
n=tk.StringVar()
u=tk.StringVar()
total_count.set("0")
y.set("0")
n.set("0")
u.set("0")
def Server():
	
	
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

	s.bind((host,port))

	s.listen(5)

	print('Server start at: %s:%s'%(host,port))
	print("wait for connection....")

	while True:
		conn,addr=s.accept()
		print("connected by"+str(addr))
		while True:
			indata=conn.recv(1024)
			if len(indata)==0:
				conn.close()
				print("client closed connection.")
			#print("rec :"+indata.decode())

			outdata=indata.decode()

			for i,data in enumerate(outdata.split(',')):
				if i==0:
					y.set(data)
				if i==1:
					n.set(data)
				if i==2:
					u.set(data)
				total_count.set(data)
			#print('i:',i,":",cal_data[i])
			
			conn.send(outdata.encode())

def thread1():
	server_t=threading.Thread(target=Server)
	server_t.start()

root.title("my web.com")
root.geometry("500x660")
fontStyle = tkFont.Font(family="Lucida Grande", size=30)




my_label=HTMLLabel(root,html="<b><h1 style='text-align:center'>口罩檢測系統!</h1></b>",height=4)

my_label.pack(fill="x",ipady=2)

interval=Label(root,height=2)
interval.pack()

total=HTMLLabel(root,html="<h1 style='text-align:center'>目前人數</h1>",height=4)
total.pack(fill="both")

total_people=tk.Label(root,textvariable=total_count,font=fontStyle,height=1)
total_people.pack(ipadx=50)

interval=Label(root,height=2)
interval.pack()

yes=HTMLLabel(root,html="<h1 style='color:green ;text-align:center'>口罩戴好</h1>",height=4)
yes.pack(fill="both")

total_people=tk.Label(root,textvariable=y,font=fontStyle,height=1)
total_people.pack(ipadx=50)

yes_people=tk.Label(root,textvariable="10",height=1)
yes_people.pack()

interval=tk.Label(root,height=1)
interval.pack()

no=HTMLLabel(root,html="<h1 style='color:red;text-align:center'>沒戴口罩</h1>",height=4)
no.pack(fill="both")

no_people=tk.Label(root,textvariable=n,font=fontStyle,height=1)
no_people.pack()

interval=Label(root,height=1)
interval.pack()


un=HTMLLabel(root,html="<h1 style='color:blue;text-align:center'>沒戴好口罩</h1>",height=4)
un.pack(fill="both")

un_people=Label(root,textvariable=u,font=fontStyle,height=1)
un_people.pack(ipadx=20)

start_detect=Button(root,text="開始偵測",height=1,font=fontStyle,command=thread1)
start_detect.pack(side='top')

root.mainloop()