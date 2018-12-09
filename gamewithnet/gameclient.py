import socket, threading, select, struct, sys
import kwek_pb2 as kwek
import math
import udp_packet_pb2 as udp_packet
import pygame
pygame.init()

host = "192.168.1.12"
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
		self.player.position.x = 50
		self.player.position.y = 50

		self.run = True

		# create a socket and connect to  server
		self.conn = self.CreateSocket()
		self.conn.setblocking(0)

		# create pygame window
		self.window = pygame.display.set_mode((500,500))
		pygame.display.set_caption("Last Kwek-Kwek")

		ckwek = udp_packet.UdpPacket.CreateKwek()
		ckwek.type = 0
		ckwek.kwek.CopyFrom(self.player)

		self.conn.sendto(ckwek.SerializeToString(), server_address)		

		while True:
			data, address = self.conn.recvfrom(4096)
			if data:
				aa = udp_packet.UdpPacket.CreateKwek()
				aa.ParseFromString(data)

				print("Kwek kwek registered. Address:",address)
				print("stats: ")
				print("name:",aa.kwek.name)
				print("id:",aa.kwek.name)
				break


		#threading.Thread(target = self.listen).start()

		#
		#threading.Thread(target = self.send).start()

#	def listen(self):
#		while True:
			#read socket, write socket, exception socket
#			rsocket, wsocket, xsocket = select.select([self.conn], [], [], 0)
			#print incoming messages
#			for sock in rsocket:
#				data = self.conn.recv(1024)
#				self.RecvPacket(data)
				
	def listen(self):
#		while self.run:
#			try:
#				data, addr = self.conn.recvfrom(1024)
#				if data:
#					print(">>",data.decode())
		while self.run:
			#read socket, write socket, exception socket
			rsocket, wsocket, xsocket = select.select([self.conn], [], [], 0)
			#print incoming messages
			#print(str(len(rsocket)))
			for sock in rsocket:
				data,addr = self.conn.recvfrom(1024)
				if data:
					#print(">>",data.decode())
					packet = udp_packet.UdpPacket()
					packet.ParseFromString(data)

					print("====>>",packet.type)
					'''if packet.type==1:
						gspacket = udp_packet.UdpPacket.GameState()
						gspacket.'''
				#self.RecvPacket(data)

	def send(self):
		kwek = udp_packet.UdpPacket.CreateKwek()
		kwek.type = udp_packet.UdpPacket.CREATE_KWEK
		kwek.kwek.CopyFrom(self.player)

		self.conn.sendto(kwek.SerializeToString(),server_address)

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
			'''
			keys = pygame.key.get_pressed()

			if keys[pygame.K_LEFT]:
				self.x -= self.velocity
				message = "new x: " + str(self.x)
				try:
					sent = self.conn.sendto(message.encode(), server_address)
				finally:
					pass
			if keys[pygame.K_RIGHT]:
				self.x += self.velocity
				message = "new x: " + str(self.x)
				try:
					sent = self.conn.sendto(message.encode(), server_address)
				finally:
					pass
			if keys[pygame.K_UP]:
				self.run = False
				#y -= velocity
				message = "q"
				try:
					sent = self.conn.sendto(message.encode(), server_address)
				finally:
					pass
			if keys[pygame.K_DOWN]:
				self.y += self.velocity
				message = "new y: " + str(self.y)
				try:
					sent = self.conn.sendto(message.encode(), server_address)
				finally:
					pass
			'''
			self.window.fill((0,0,0))
			cx,cy = self.followCursor()
			print("x:",cx,", y:",cy)
			message = "x: "+str(cx)+", y: "+str(cy)
			#message = "x:"+str(self.x)+";; y:"+str(self.y)
			sent = self.conn.sendto(message.encode(), server_address)
			#pygame.draw.rect(self.window,(255,0,0),(self.x,self.y,self.width,self.height))
			pygame.display.update()

		self.conn.close()
		pygame.quit()

	def followCursor(self):
		#cursor_x, cursor_y = pygame.mouse.get_pos()
		return pygame.mouse.get_pos()
		'''dx = cursor_x - self.x
		dy = cursor_y - self.y
		distance = math.sqrt(dx*dx + dy*dy)
		dx /= distance
		dy /= distance
		dx *= self.speed
		dy *= self.speed
		self.x += dx
		self.y += dy
		if self.x >= screen_width-50:
		    self.x = screen_width-50
		if self.y >= screen_height-50:
		    self.y = screen_height-50

		#self.rect.center=(self.x,self.y)
		#surface.blit(self.image, (self.x-(self.rect.width/2), self.y-(self.rect.height)/2))
		pygame.draw.rect(self.window,(255,0,0),(self.x,self.y,self.width,self.height))'''
		#pygame.display.update()

	def CreateKwek(self,usr):
		nkwek = kwek.Kwek()
		nkwek.name = usr
		return nkwek

	def CreateSocket(self):
		return socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

if __name__ == "__main__":
	usr = input("name: ")
	Client(usr)
