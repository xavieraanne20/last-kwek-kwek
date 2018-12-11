'''
ABOUT THE PROGRAM:
	NAME: KWEK CHAT
	PURPORSE:	HOST SETS THE CREATIION OF LOBBY THEN  CAN PROCEED TO CHAT
'''
import socket, threading, select, struct
import tcp_packet_pb2 as tcp_packet
import player_pb2 as play
#USED TKINTER FOR USER INTERFACE
import tkinter as tk
from tkinter import *
import os
from tkinter.simpledialog import askstring,askinteger

host = "202.92.144.45"
port = 80

top = tk.Tk()
top.configure(background="black")
top.title("Kwek Messenger")
top.geometry("300x600")
max_p = 5

def CreateLobbyPacket(sock):
	packet = tcp_packet.TcpPacket.CreateLobbyPacket(
		type = tcp_packet.TcpPacket.CREATE_LOBBY,
		max_players = max_p
	)
	sock.send(packet.SerializeToString())
	data=sock.recv(1024)
	packet.ParseFromString(data)
	lobby_id = packet.lobby_id
	return lobby_id

#FOR GETTING THE USER'S MSG
def proceed(even=None):
	message = entry.get()
	if (message=="show_players" or message=="show players" or message=="SHOW PLAYERS"):

		packet = tcp_packet.TcpPacket.PlayerListPacket(
			type = tcp_packet.TcpPacket.PLAYER_LIST
		)
	else:
		packet =tcp_packet.TcpPacket.ChatPacket(
			type= tcp_packet.TcpPacket.CHAT,
			lobby_id = lobby_id,		
			player=player,
			message=message
		)
	sock.send(packet.SerializeToString())
	entry.delete(0, tk.END)

#GETS THE USER'S NAME AND THE LOBBY ID (S)HE WANTS TO JOIN
def getPlayer():
	global player,lobby_id,msg,playerList,packetListener,data,max_p
	player=play.Player(	
		name = playername.get()
	)
	lobby_id = CreateLobbyPacket(sock)
	labelID['text'] = "LOBBY ID:" +lobby_id
	mainPage.withdraw()
	player = ConnectPacket(sock,player,lobby_id)
	playerList=PlayerListPacket()
	packetListener = threading.Thread(target=RecvPacket,args=(sock,player),daemon=True)
	packetListener.start()

#----------HOST WINDOW
mainPage=tk.Toplevel(bg="black")
mainPage.title("HOST WINDOW")
mainPage.geometry('300x80')
mainPage.attributes('-topmost','true')

a = tk.Label(mainPage,text="KWEK CHAT",bg="black",fg="orange").grid(row=2,column=1)
z = tk.Label(mainPage, text="Player name: ",bg="black",fg="orange").grid(row=3)
playername = tk.Entry(mainPage, width=20, fg="black",bg="orange",bd=0)
playername.grid(row=3, column=1)
enter1 = tk.Button(mainPage,text='Enter game',activebackground="orange",activeforeground="white",bd=0,bg="black",fg="orange",command=getPlayer).grid(row=5, column=1)
#----------HOST WINDOW

#CHAT INPUT BOX FOR THE  MESSAGE
chatarea = tk.Text(top, state='disabled', height=35, width=55, bg="black",fg="orange",bd=5)
chatarea.pack()
entry = tk.Entry(top,  bd=2, width=50,bg="orange",fg="black")
entry.pack()
button = tk.Button(top,bd=3,bg='orange',fg="black",relief="ridge",activebackground="black",activeforeground="orange",text='Send Message',command=proceed)
top.bind('<Return>', proceed)
button.pack()


def __init__(name):
	# create a protobuf player

	player = CreatePlayer(name)
	lobby_id = ""

	# create a socket and connect to  server
	conn = CreateSocket()
	ConnectToServer()
	threading.Thread(target = listen).start()

	threading.Thread(target = send).start()

			

def send():
	#HOST ENTERS LOBBY
	while True:
		disconn = False
		if(lobby_id==""):
			
			lobID = input("Lobby ID: ")
			conn.send(ConnectPacket(lobID))
			lobby_id = "."
		else: 
			msg = input()
			
			if msg == "exit":
				# Send disconnect packet
				conn.send(DisconnectPacket())
				exit()
			elif msg == "show_players":
				conn.send(PlayerListPacket())

			else:
				conn.send(ChatPacket(msg))


def ChatPacket(data):
	chatp = tcp_packet.TcpPacket.ChatPacket()
	chatp.type = tcp_packet.TcpPacket.CHAT
	chatp.message = data
	chatp.player.CopyFrom(player)

	return chatp.SerializeToString()

def PlayerListPacket():
	packet = tcp_packet.TcpPacket.PlayerListPacket(
		type = tcp_packet.TcpPacket.PLAYER_LIST
	)
	return packet.SerializeToString()

def DisconnectPacket():
	packet = tcp_packet.TcpPacket.DisconnectPacket(	
		type = tcp_packet.TcpPacket.DISCONNECT
	)
	return packet.SerializeToString()


def ConnectPacket(sock,player,lobby_id):
	packet = tcp_packet.TcpPacket.ConnectPacket(
		type = tcp_packet.TcpPacket.CONNECT,
		player= player,
		lobby_id = lobby_id
	)
	sock.send(packet.SerializeToString())
	data=sock.recv(1024)
	packet.ParseFromString(data)
	return packet.player

#RECEIVE PACKET, IDENTIFY IF WHAT KIND OF PACKET IS BEING SENT BY SENDER
def RecvPacket(sock,player):
	
	packet = tcp_packet.TcpPacket()
	while True:
		data = sock.recv(1024)	
		packet.ParseFromString(data)
		#USER DISCONNECTED FROM THE CHAT
		if packet.type == 0:
			ret = tcp_packet.TcpPacket.DisconnectPacket()
			ret.ParseFromString(data)
			if ret.player.name=="":
				exit()
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,ret.player.name + " has disconnected [" + str(ret.update) + "]\n")
			chatarea.configure(state = 'disabled')	
		
		#A NEW USER ENTERED THE LOBBY	
		elif packet.type == 1:
			ret = tcp_packet.TcpPacket.ConnectPacket()
			ret.ParseFromString(data)
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,ret.player.name + ' has entered the lobby. \n')
			chatarea.configure(state = 'disabled')
			lobby_id = ret.lobby_id

		#HOST CREATED LOBBY PACKET 
		elif packet.type == 2:
			ret = tcp_packet.TcpPacket.CreateLobbyPacket()
			ret.ParseFromString(data)
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,'Created lobby:' + ret.lobby_id + "\n")
			chatarea.configure(state = 'disabled')
			
		#USER'S MESSAGE SENT	
		elif packet.type == 3:
			ret = tcp_packet.TcpPacket.ChatPacket()
			ret.ParseFromString(data)
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,ret.player.name + ':\t' + ret.message + "\n")
			chatarea.configure(state = 'disabled')
		
		#SHOW PLAYER LIST
		elif packet.type == 4:
			ret = tcp_packet.TcpPacket.PlayerListPacket()
			ret.ParseFromString(data)
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,"Player list:\n")
			chatarea.configure(state = 'disabled')
			for p in ret.player_list:
				chatarea.configure(state = 'normal')
				chatarea.insert(tk.END, "\t> " + p.name + "; id:" + p.id + "\n")
				chatarea.configure(state = 'disabled')
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,"Num of Players in lobby" + str(len(ret.player_list)) + "\n")
			chatarea.configure(state = 'disabled')

		#ERROR MESSAGES			
		elif packet.type == 5:
			ret = tcp_packet.TcpPacket.ErrLdnePacket()
			ret.ParseFromString(data)
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,"!!! "+ret.err_message+" !!!\n")
			chatarea.configure(state = 'disabled')
		
		elif packet.type == 6:
			ret = tcp_packet.TcpPacket.ErrLfullPacket()
			ret.ParseFromString(data)
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,"!!! "+ret.err_message+" !!!\n")
			chatarea.configure(state = 'disabled')
		
		elif packet.type == 7:
			ret = tcp_packet.TcpPacket.ErrPacket()
			ret.ParseFromString(data)
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,"!!! "+ret.err_message+" !!!\n")
			chatarea.configure(state = 'disabled')

#CREATES NEW PLAYER
def CreatePlayer(player):
	nplayer = player.Player()
	nplayer.name = player
	return nplayer

def CreateSocket():
	return socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def ConnectToServer():
	conn.connect((host,port))


messages_frame = tk.Frame(top)
labelID = tk.Label(top,text="",font=('Helvetica', '15'), fg="orange",bg="black")
labelID.pack()

player=""

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("202.92.144.45", 80))



top.mainloop()

