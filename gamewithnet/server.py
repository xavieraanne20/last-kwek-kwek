import socket
import sys, math
import kwek_pb2 as kwek
import random, string
import udp_packet_pb2 as udp_packet

host = "0.0.0.0"
port = 5001

adrs = []
#kweks = []
kwek_ids = []

game_state = udp_packet.UdpPacket.GameState()
game_state.type = 1


def randomstr(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def handleMotion(x,y,kwek):
	dx = x - kwek.position.x
	dy = y - kwek.position.y
	print("1:",str(dx),str(dy))
	distance = math.sqrt(dx*dx + dy*dy)
	dx /= distance
	dy /= distance
	print("2:",str(dx),str(dy))
	dx *= kwek.velocity
	dy *= kwek.velocity
	print("3:",str(dx),str(dy))
	kwek.position.x += dx
	kwek.position.y += dy
	screen_width = screen_height = 500
	#print("new:",str(kwek.position.x),str(kwek.position.y))
	#if kwek.position.x >= screen_width-50:
	#	kwek.position.x = screen_width-50
	#if kwek.position.y >= screen_height-50:
	#	kwek.position.y = screen_height-50
	#kwek.position.x -= kwek.dimension.width/2
	#kwek.position.y -= kwek.dimension.height/2
	print("new:",str(kwek.position.x),str(kwek.position.y))
	#surface.blit(self.image, (self.x-(self.rect.width/2), self.y-(self.rect.height)/2))

	#print("old:",str(x),str(y))
	
	#return float(x),float(y)

def handlePacket(sock,adress,packet):
	if packet.type==0:
		c_kwek = udp_packet.UdpPacket.CreateKwek()
		c_kwek.ParseFromString(data)

		while True:
			k_id = randomstr(4)
			if k_id not in kwek_ids:
				kwek_ids.append(k_id)
				c_kwek.kwek.id = k_id
				break
		if c_kwek.kwek not in game_state.kweks:
			kk = game_state.kweks.add()
			kk.CopyFrom(c_kwek.kwek)
			print("-+-+->",len(game_state.kweks))
		#kweks.append(c_kwek.kwek)
		#print(str(len(kweks)))

		sock.sendto(c_kwek.SerializeToString(),address)
	if packet.type == 2:
		move = udp_packet.UdpPacket.Motion()
		move.ParseFromString(data)

		for k in game_state.kweks:
			if k.id == move.kwek.id:
				print("found-----------")
				#newx, newy = 
				handleMotion(move.x,move.y,move.kwek)
				k.CopyFrom(move.kwek)
				#k.position.x = move.x
				#k.position.y = move.y
			 # CHECK FOR COLLISIONS HERE
			 # COLLISIONS WITH BACTERIA ETC

		sock.sendto(game_state.SerializeToString(),address)





# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = (host,port)
sock.bind(server_address)
print("Server running.")
count = 0
while True:
	#start receiving messages
	data, address = sock.recvfrom(4096)

	if data:
		# create generic UDP Packet
		if address not in adrs:
			# add address to list of clients
			adrs.append(address)
		try:
			packet = udp_packet.UdpPacket()
			packet.ParseFromString(data)

			handlePacket(sock,address,packet)
		except:
			print(";-->",data.decode())
			sendback = "From " + str(address) + ": " + data.decode()
			for a in adrs:
				sock.sendto(sendback.encode(),a)
			if data.decode() == "q":
				break;

sock.close()