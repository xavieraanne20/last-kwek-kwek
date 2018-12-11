import socket, threading, select, struct, sys
import kwek_pb2 as kwek
import math
import udp_packet_pb2 as udp_packet
import pygame, sys
pygame.init()

host = sys.argv[1]
port = 5001

server_address = (host,port)

class Client:

	def __init__(self,name):
		# create a protobuf player
		self.name = name

		#local copy of kwekwek innstance
		self.player = self.CreateKwek(name)
		self.player.name = name
		self.player.points = 20
		self.player.dimension.height = 60
		self.player.dimension.width = 40
		self.player.position.x = 250
		self.player.position.y = 250
		self.player.velocity = 6

		self.run = True

		# create a socket and connect to  server
		self.conn = self.CreateSocket()
		#self.conn.setblocking(0)

		# create pygame window
		self.window = pygame.display.set_mode((500,500))
		pygame.display.set_caption("Last Kwek-Kwek")

		ckwek = udp_packet.UdpPacket.CreateKwek()
		ckwek.type = 0
		ckwek.kwek.CopyFrom(self.player)

		self.conn.sendto(ckwek.SerializeToString(), server_address)		

		
		data, address = self.conn.recvfrom(4096)
		if data:
			# Player registered to server
			aa = udp_packet.UdpPacket.CreateKwek()
			aa.ParseFromString(data)
			self.player.CopyFrom(aa.kwek)




		threading.Thread(target = self.listen).start()

		#
		threading.Thread(target = self.send).start()
				
	def listen(self):
		while self.run:
			#read socket, write socket, exception socket
			rsocket, wsocket, xsocket = select.select([self.conn], [], [], 0)
			#print incoming messages
			#print(str(len(rsocket)))
			for sock in rsocket:
				data,addr = self.conn.recvfrom(1024)
				if data:
					#print(">>",data.decode())
					try:
						packet = udp_packet.UdpPacket()
						packet.ParseFromString(data)

						if packet.type == 1:
							gs = udp_packet.UdpPacket.GameState()
							gs.ParseFromString(data)


							self.window.fill((0,0,0))
							for k in gs.kweks:
								#print(k.name)
								#print("PPPPPPPPPPPPPos x:",k,position.x,"y:",k.position.y)
								if k.id == self.player.id:
									self.player.CopyFrom(k)
								pygame.draw.rect(self.window,(255,0,0),(k.position.x,k.position.y,k.dimension.width,k.dimension.height))
							pygame.display.update()
					except:
						print(data.decode())

	def send(self):
		while self.run:
			# 0.1 seconds
			pygame.time.delay(100) 

			# events 
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False

			keys = pygame.key.get_pressed()
			if keys[pygame.K_UP]:
				self.run = False

			cx,cy = self.followCursor()
			#message = "x: "+str(cx)+", y: "+str(cy)

			# create a motion packet
			mpacket = udp_packet.UdpPacket.Motion()
			mpacket.type = 2
			mpacket.kwek.CopyFrom(self.player)
			mpacket.x = cx
			mpacket.y = cy

			sent = self.conn.sendto(mpacket.SerializeToString(), server_address)

		self.conn.close()
		pygame.quit()

	def followCursor(self):
		return pygame.mouse.get_pos()

	def CreateKwek(self,usr):
		nkwek = kwek.Kwek()
		nkwek.name = usr
		return nkwek

	def CreateSocket(self):
		return socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

if __name__ == "__main__":
	usr = input("name: ")
	Client(usr)
