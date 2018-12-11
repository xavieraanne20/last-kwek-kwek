import socket, threading, select, struct
import tcp_packet_pb2 as tcp_packet
import player_pb2 as play
"GUI"
import tkinter as tk
from tkinter import *
import os
from tkinter.simpledialog import askstring,askinteger

host = "202.92.144.45"
port = 80
top = tk.Tk()
top.title("Kwek Messenger")
top.geometry("300x600")
globalmax_p=5
def proceed(even=None):
	message = entry.get()
	packet =tcp_packet.TcpPacket.ChatPacket(
		type= tcp_packet.TcpPacket.CHAT,
		lobby_id = lobby_id,		
		player=player,
		message=message
		#print(messages_frame)
	)
	sock.send(packet.SerializeToString())
	entry.delete(0, tk.END)


def getPlayer():
	global player,lobby_id,msg,playerList,packetListener,data
	player=play.Player(	
		name = playername.get()
	)
	

	lobby_id = lobid.get()
	labelID['text'] = "LOBBY ID:" +lobby_id
	mainPage.withdraw()
	player = ConnectPacket(sock,player,lobby_id)
	playerList=PlayerListPacket()
	packetListener = threading.Thread(target=RecvPacket,args=(sock,player),daemon=True)
	packetListener.start()

def getRad():
	global lobby_id
	radio = var.get()
	if (radio==	1):
		print("hello")
		lobby_id = lobid.get()
	elif (radio ==2):
		print("not hello")
		lobby_id = CreateLobbyPacket(sock)

mainPage=tk.Toplevel()
mainPage.title("PLEASE ENTER DETAILS TO PROCEED")
mainPage.geometry('300x200')
mainPage.attributes('-topmost','true')


w = tk.Label(mainPage, text="Lobby ID: ").grid(row=2)
lobid= tk.Entry(mainPage, width=20, fg="blue")
lobid.grid(row=2, column=1)
z = tk.Label(mainPage, text="Player name: ").grid(row=3)
playername = tk.Entry(mainPage, width=20, fg="blue")
playername.grid(row=3, column=1)
enter1 = tk.Button(mainPage,text='Enter game',command=getPlayer).grid(row=5, column=1)
chatarea = tk.Text(top, state='disabled', height=35, width=55, fg="blue")
chatarea.pack()
entry = tk.Entry(top,  bd=5, width=50)
entry.pack()
button = tk.Button(top,text='Submit',command=proceed)
top.bind('<Return>', proceed)

button.pack()
#R1.pack( anchor = W )
#R2.pack( anchor = W )
def __init__(name):
	# create a protobuf player

	player = CreatePlayer(name)
	lobby_id = ""

	# create a socket and connect to  server
	conn = CreateSocket()
	ConnectToServer()

	threading.Thread(target = listen).start()

	#
	threading.Thread(target = send).start()

#def listen():
	
			

def send():
	#CLIENT ENTER LOBBY
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
	plist = tcp_packet.TcpPacket.PlayerListPacket()
	plist.type = tcp_packet.TcpPacket.PLAYER_LIST

	return plist.SerializeToString()

def DisconnectPacket():
	dc_packet = tcp_packet.TcpPacket.DisconnectPacket()				
	dc_packet.type = tcp_packet.TcpPacket.DISCONNECT

	return dc_packet.SerializeToString()


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


def RecvPacket(sock,player):
	
	packet = tcp_packet.TcpPacket()
	while True:
		data = sock.recv(1024)	
		packet.ParseFromString(data)
		if packet.type == 0:
			ret = tcp_packet.TcpPacket.DisconnectPacket()
			ret.ParseFromString(data)
			if ret.player.name=="":
				exit()
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,ret.player.name + " has disconnected [" + str(ret.update) + "]\n")
			chatarea.configure(state = 'disabled')	
			#print(ret.player.name + " has disconnected [" + str(ret.update) + "]")
		elif packet.type == 1:
			ret = tcp_packet.TcpPacket.ConnectPacket()
			ret.ParseFromString(data)
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,ret.player.name + 'has entered the lobby. \n')
			chatarea.configure(state = 'disabled')
			#print(ret.player.name + " has entered the lobby.")
			lobby_id = ret.lobby_id
		elif packet.type == 2:
			ret = tcp_packet.TcpPacket.CreateLobbyPacket()
			ret.ParseFromString(data)
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,'Created lobby:' + ret.lobby_id + "\n")
			chatarea.configure(state = 'disabled')
			#print("Created lobby: " + ret.lobby_id)
		elif packet.type == 3:
			ret = tcp_packet.TcpPacket.ChatPacket()
			ret.ParseFromString(data)
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,ret.player.name + '>>' + ret.message + "\n")
			chatarea.configure(state = 'disabled')
			#print(ret.player.name + ">> " + ret.message)
		elif packet.type == 4:
			ret = tcp_packet.TcpPacket.PlayerListPacket()
			ret.ParseFromString(data)
			#print(ret.player_list)
			#print("\nPlayer list:")
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,"Player list:\n")
			chatarea.configure(state = 'disabled')
			for p in ret.player_list:
			#	print("\t> "+p.name+"; id: "+p.id)
				chatarea.configure(state = 'normal')
				chatarea.insert(tk.END, "\t>" + p.name + "; id:" + p.id + "\n")
				chatarea.configure(state = 'disabled')
			#print("Num of Players in lobby: "+str(len(ret.player_list))+"\n")
			chatarea.configure(state = 'normal')
			chatarea.insert("Num of Players in lobby" + str(len(ret.player_list)) + "\n")
			chatarea.configure(state = 'disabled')
		elif packet.type == 5:
			ret = tcp_packet.TcpPacket.ErrLdnePacket()
			ret.ParseFromString(data)
			#print("!!! "+ret.err_message+" !!!")
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,"!!! "+ret.err_message+" !!!\n")
			chatarea.configure(state = 'disabled')
		elif packet.type == 6:
			ret = tcp_packet.TcpPacket.ErrLfullPacket()
			ret.ParseFromString(data)
			#print("!!! "+ret.err_message+" !!!")
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,"!!! "+ret.err_message+" !!!\n")
			chatarea.configure(state = 'disabled')
		elif packet.type == 7:
			ret = tcp_packet.TcpPacket.ErrPacket()
			ret.ParseFromString(data)
			#print("!!! "+ret.err_message+" !!!")
			chatarea.configure(state = 'normal')
			chatarea.insert(tk.END,"!!! "+ret.err_message+" !!!\n")
			chatarea.configure(state = 'disabled')

def CreateLobbyPacket(sock):
	packet = tcp_packet.TcpPacket.CreateLobbyPacket()(
		type = tcp_packet.TcpPacket.CREATE_LOBBY,
		max_players = max_p
	)
	sock.send(packet.SerializeToString())
	data=sock.recv(1024)
	packet.ParseFromString(data)
	obby_id = packet.lobby_id
	return lobby_id


def CreatePlayer(player):
	nplayer = player.Player()
	nplayer.name = player
	return nplayer

def CreateSocket():
	return socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def ConnectToServer():
	conn.connect((host,port))





messages_frame = tk.Frame(top)
labelID = tk.Label(top,text="",font=('Helvetica', '15'), fg="blue")
labelID.pack()

player=""

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("202.92.144.45", 80))



top.mainloop()

