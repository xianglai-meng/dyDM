# codig=utf-8

import re
import time
import struct
import socket

def connect():
	host=socket.gethostbyname('danmu.douyu.com')
	port=8602
	global client
	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	client.connect((host,port))

def send_msg(msgstr):
	msg=msgstr.encode('utf-8')
	data_length=len(msgstr)+8
	code=689
	msgHead=int.to_bytes(data_length,4,'little')+int.to_bytes(data_length,4,'little')+int.to_bytes(code,4,'little')
	client.send(msgHead)
	client.send(msg)

def receive_danmu(room_id):
	login ='type@=loginreq/roomid@=%s/\0'%room_id
	print(login)
	send_msg(login)
	time.sleep(1)
	joingroup='type@=joingroup/rid@=%s/gid@=-9999/\0'%room_id
	print(joingroup)
	send_msg(joingroup)
	time.sleep(1)

	while True:
		content = client.recv(1024)
		time.sleep(0.1)
		if judge_chatmsg(content):
			nickname=nick_name(content)
			chatmsg=chat_msg(content)
			print('[danmu]%s:%s'%(nickname,chatmsg))
		else:
			pass

def nick_name(content):
	pattern=b'nn@=(.*?)/'	
	#print('nickname:%s'%pattern)	
	nick_name=re.findall(pattern,content)	

	if(len(nick_name)>0):
		return nick_name[0].decode('utf-8')
	else:	
		return nick_name	

def chat_msg(content):
	pattern=b'txt@=(.*?)/'
	#print('msg:%s'%pattern)	
	chatmsg=re.findall(pattern,content)
	msglen =len(chatmsg)
	#print(msglen)
	if(msglen>0):
		return chatmsg[0].decode('utf-8')
	else:			
		return chatmsg	

def judge_chatmsg(content):
	pattern=re.compile(b'type@=(.*)/rid@')		
	data_type=pattern.findall(content)

	try:
		if data_type[0]==b'chatmsg':			 
			return True
		else:
			return False 
	except Exception as e:
		return	False


if __name__ == '__main__':
	connect()
	receive_danmu(9999)