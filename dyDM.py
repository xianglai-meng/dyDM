# codig=utf-8

import re
import time
import struct
import socket

def connect():
	host=socket.gethostbyname('openbarrage.douyutv.com')
	port=8601
	global client
	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	client.connect((host,port))

def send_msg(msg):
	data_length=len(msg)-8
	code=689
	msgHead=struct.pack('<i',data_length)\
		+struct.pack('<i',data_length)+struct.pack('<i',code)
	client.send(msgHead)
	print(msgHead)
	send=0
	while send<len(msg):
		tn=client.send(msg[send:])
		send=send+tn

def receive_danmu(room_id):
	login ='type@loginreq/roomid@%s/\0'%room_id
	login=login.encode('utf-8')
	print(login)
	send_msg(login)
	joingroup='type@=joingroup/rid@=%s/gid@=-9999/\0'%room_id
	joingroup=joingroup.encode('utf-8')
	print(joingroup)
	send_msg(joingroup)
	while True:
		content = client.recv(1024)
		print(content)
		if judge_chatmsg(content):
			nickname=nick_name(content)
			chatmsg=chat_msg(content)
			print('[danmu]%s:%s')%(nickname,chatmsg)
		else:
			pass

def nick_name(content):
	pattern=re.compile(r'nn@=(.+*)/')		
	nick_name=pattern.findall(content[0])
	return nick_name

def chat_msg(content):
	pattern=re.compile(r'txt@=(.*)/')
	chatmsg=pattern.findall(content[0])
	return chatmsg	

def judge_chatmsg(content):
	pattern=re.compile(r'type@=(.*)/rid@')
	print(content,'pd')
	data_type=pattern.findall(content)
	try:
		if data_type[0]=='chatmsg':
			print('true')  
			return True
		else:
			print('false')  
			return False 
	except Exception as e:
		return	False


if __name__ == '__main__':
	connect()
	receive_danmu(1972046)