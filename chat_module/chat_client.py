import socket, threading, select, struct
import tcp_packet_pb2 as tcp_packet
from proto import player_pb2 as player

host = "202.92.144.45"
port = 80

class Client:

	def __init__(self,name):
		# create a protobuf player
		self.player = self.CreatePlayer(name)
		self.lobby_id = ""

		# create a socket and connect to  server
		self.conn = self.CreateSocket()
		self.ConnectToServer()

		threading.Thread(target = self.listen).start()

		#
		threading.Thread(target = self.send).start()

	def listen(self):
		while True:
			#read socket, write socket, exception socket
			rsocket, wsocket, xsocket = select.select([self.conn], [], [], 0)
			#print incoming messages
			for sock in rsocket:
				data = self.conn.recv(1024)
				self.RecvPacket(data)
				
	
	def send(self):
		while True:
			disconn = False
			if(self.lobby_id==""):
				print("[1] Create Lobby")
				print("[2] Connect to Lobby")
				choice = int(input("Choice: "))

				#create a new lobby
				if choice == 1:
					max_p = int(input("Max # of players: "))
					self.conn.send(self.CreateLobbyPacket(max_p))

				#connect to existing lobby
				elif choice == 2:
					lobID = input("Lobby ID: ")
					self.conn.send(self.ConnectPacket(lobID))
					self.lobby_id = "."
			else: 
				msg = input()
				if msg == "exit":
					# Send disconnect packet
					self.conn.send(self.DisconnectPacket())
					exit()
				elif msg == "show_players":
					self.conn.send(self.PlayerListPacket())

				else:
					self.conn.send(self.ChatPacket(msg))

	
	def ChatPacket(self,data):
		chatp = tcp_packet.TcpPacket.ChatPacket()
		chatp.type = tcp_packet.TcpPacket.CHAT
		chatp.message = data
		chatp.player.CopyFrom(self.player)

		return chatp.SerializeToString()

	def PlayerListPacket(self):
		plist = tcp_packet.TcpPacket.PlayerListPacket()
		plist.type = tcp_packet.TcpPacket.PLAYER_LIST

		return plist.SerializeToString()

	def DisconnectPacket(self):
		dc_packet = tcp_packet.TcpPacket.DisconnectPacket()				
		dc_packet.type = tcp_packet.TcpPacket.DISCONNECT

		return dc_packet.SerializeToString()

	def ConnectPacket(self,lobID):
		con_packet = tcp_packet.TcpPacket.ConnectPacket()
		con_packet.type = tcp_packet.TcpPacket.CONNECT
		con_packet.player.CopyFrom(self.player)	
		con_packet.lobby_id = lobID		

		return con_packet.SerializeToString()

	def RecvPacket(self,data):
		packet = tcp_packet.TcpPacket()
		packet.ParseFromString(data)

		if packet.type == 0:
			ret = tcp_packet.TcpPacket.DisconnectPacket()
			ret.ParseFromString(data)
			if ret.player.name=="":
				exit()
			print(ret.player.name + " has disconnected [" + str(ret.update) + "]")
		elif packet.type == 1:
			ret = tcp_packet.TcpPacket.ConnectPacket()
			ret.ParseFromString(data)
			print(ret.player.name + " has entered the lobby.")
			self.lobby_id = ret.lobby_id
		elif packet.type == 2:
			ret = tcp_packet.TcpPacket.CreateLobbyPacket()
			ret.ParseFromString(data)
			print("Created lobby: " + ret.lobby_id)
		elif packet.type == 3:
			ret = tcp_packet.TcpPacket.ChatPacket()
			ret.ParseFromString(data)
			print(ret.player.name + ">> " + ret.message)
		elif packet.type == 4:
			ret = tcp_packet.TcpPacket.PlayerListPacket()
			ret.ParseFromString(data)
			#print(ret.player_list)
			print("\nPlayer list:")
			for p in ret.player_list:
				print("\t> "+p.name+"; id: "+p.id)
			print("Num of Players in lobby: "+str(len(ret.player_list))+"\n")
		elif packet.type == 5:
			ret = tcp_packet.TcpPacket.ErrLdnePacket()
			ret.ParseFromString(data)
			print("!!! "+ret.err_message+" !!!")
		elif packet.type == 6:
			ret = tcp_packet.TcpPacket.ErrLfullPacket()
			ret.ParseFromString(data)
			print("!!! "+ret.err_message+" !!!")
		elif packet.type == 7:
			ret = tcp_packet.TcpPacket.ErrPacket()
			ret.ParseFromString(data)
			print("!!! "+ret.err_message+" !!!")

	def CreateLobbyPacket(self,max_p):
		lobby_packet = tcp_packet.TcpPacket.CreateLobbyPacket()
		lobby_packet.type = tcp_packet.TcpPacket.CREATE_LOBBY
		lobby_packet.max_players = max_p

		return lobby_packet.SerializeToString()

	def CreatePlayer(self,usr):
		nplayer = player.Player()
		nplayer.name = usr
		return nplayer

	def CreateSocket(self):
		return socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	def ConnectToServer(self):
		self.conn.connect((host,port))

if __name__ == "__main__":
	usr = input("name: ")
	Client(usr)
	#usr = CreatePlayer(usr)

	#conn = CreateSocket()
	#conn.connect((host,port))

	#print("Connected to "+ host)

	#conn.close()
