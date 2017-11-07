import sys
import socket
import string
import time
import configparser
def isDEC(s):
	try:
		int(s)
		return 1
	except ValueError:
		try:
			int(s,16)
			return 0
		except ValueError:
			return -1
def inset(i,j,k,s):
	tem=""		
	if(i==0):
		ti = s[0]
	else:
		ti = s[0:i]
		if(ti[0]=="0"):
			return 0,tem
		tii = int(ti)
		if(tii<0 or tii>255):
			return 0,tem
	if((j-i)==1):
		tj = s[i]
	else:
		tj = s[i:j]
		if(tj[0]=="0"):
			return 0,tem
		tjj = int(tj)
		if(tjj<0 or tjj>255):
			return 0,tem
	if((k-j)==1):
		tk = s[j]
	else:
		tk = s[j:k]
		if(tk[0]=="0"):
			return 0,tem
		tkk = int(tk)
		if(tkk<0 or tkk>255):
			return 0,tem
	if((n-k)==1):
		te = s[k]
	else:
		te = s[k:n]
		if(te[0]=="0"):
			return 0,tem
		tee = int(te)
		if(tee<0 or tee>255):
			return 0,tem
	tem=ti+"."+tj+"."+tk+"."+te
	return 1,tem

HOST = "irc.freenode.net"
PORT = 6667
NICK = "CXBOT"
IDENT = "CX"
REALNAME = "CLAIRE"


config = configparser.ConfigParser()
config.readfp(open(r'hw1.config'))
chan= config.get('config', 'CHAN')
chan = str.split(chan,"\'")
CHAN=chan[1]
readbuffer = ""
irc=socket.socket( )
irc.connect((HOST, PORT))
irc.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
irc.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))
irc.send(bytes("JOIN %s\r\n" % CHAN, "UTF-8"))
irc.send(bytes("PRIVMSG %s :Hello! I am robot\r\n"%CHAN,"UTF-8"))

while 1:
	readbuffer = readbuffer+irc.recv(1024).decode("UTF-8")
	temp = str.split(readbuffer,"\n")
	readbuffer=temp.pop()
	for line in temp:
		line = str.rstrip(line)
		line = str.split(line)
		if(line[0]=='PING'):
			irc.send(bytes("PONG %s\r\n"%line[1],"UTF-8"))
		if(line[1]=="QUIT"):
			irc.send(bytes("PRIVMSG %s :Goodbye~~ \r\n"%CHAN,"UTF-8"))
		if(len(line)>3):
			if(line[3]==":@repeat"):
				tt=""
				for i in range(4,len(line)):
					if(i==4):
						tt=line[4]
					else:
						tt=tt+" "+line[i]
				#print(tt)
				
				irc.send(bytes("PRIVMSG %s :%s \r\n"%(CHAN,tt),"UTF-8"))
			if(line[3]==":@convert"):
				tem=line[4]
				if(isDEC(tem)==1):#DEC
					dd = int(tem)
					con = hex(dd)
					
					irc.send(bytes("PRIVMSG %s :%s \r\n"%(CHAN,con),"UTF-8"))
				elif(isDEC(tem)==0):#hex
					hh = int(tem,16)
					con = str(hh)
					irc.send(bytes("PRIVMSG %s :%s \r\n"%(CHAN,con),"UTF-8"))
				else:
					irc.send(bytes("PRIVMSG %s :Tips:@convert <Number> \r\n"%CHAN,"UTF-8"))
			if(line[3]==":@help"):
				irc.send(bytes("PRIVMSG %s :@repeat <Message> \r\n"%CHAN,"UTF-8"))
				irc.send(bytes("PRIVMSG %s :@convert <Number> \r\n"%CHAN,"UTF-8"))
				irc.send(bytes("PRIVMSG %s :@ip <String> \r\n"%CHAN,"UTF-8"))
			if(line[3]==":@ip"):
				if(len(line)==5):
					if(isDEC(line[4])==1):

						n = len(line[4])
						tem = line[4]
						inuse = n-1
						if(inuse<3):
							irc.send(bytes("PRIVMSG %s :0 \r\n"%CHAN,"UTF-8"))
						else:

							put=[]
						
							c = 0
							
							for i in range(1,n):	
								for j in range(i+1,n):	
									for k in range(j+1,n):
										ctr,tt=inset(i,j,k,tem)
										if(ctr==1):
											put.append(tt)
											c = c + 1


							irc.send(bytes("PRIVMSG %s :%d \r\n"%(CHAN,c),"UTF-8"))
							for ans in put:
								irc.send(bytes("PRIVMSG %s :%s \r\n"%(CHAN,ans),"UTF-8"))
									#irc.send(bytes("PRIVMSG %s :%s \r\n"%(CHAN,con),"UTF-8"))
								time.sleep(1)
				else:
					irc.send(bytes("PRIVMSG %s :Tips:@ip <Number> \r\n"%CHAN,"UTF-8"))	
			
		print(line)