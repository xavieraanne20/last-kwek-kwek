import socket
import sys
import kwek_pb2 as kwek
import random, string
import udp_packet_pb2 as udp_packet

def randomstr(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

host = "0.0.0.0"
port = 5001
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = (host,port)

sock.bind(server_address)
#sock.setblocking(0)

players = []
kweks = {}

game_state = udp_packet.UdpPacket.GameState()
game_state.type = 1

while True:
	print('\nwaiting to receive message')
	data, address = sock.recvfrom(4096)
	#break
	'''
	if data:
		packet = udp_packet.UdpPacket()
		packet.ParseFromString(data)

		print("huh:",packet.type)
		if packet.type == 0:
			if address not in players:
				#addr = (address,port)
				#print("added ",address)
				players.append(address)

			c_kwek = udp_packet.UdpPacket.CreateKwek()
			c_kwek.ParseFromString(data)
			c_kwek.kwek.id = randomstr(3)

			kwek = c_kwek.kwek
			kweks[kwek.id] = address

			newkwek = game_state.kweks.add()
			newkwek.name = kwek.name
			newkwek.id = kwek.id
		elif packet.type == 2:
			motion = udp_packet.UdpPacket.Motion()
			motion.ParseFromString(data)

			for k in game_state.kweks:
				if k.id == motion.kwek.id:
					k.position.x = motion.kwek.position.x
					k.position.y = motion.kwek.position.y

		
	for k in kweks:
		print(k,"--",kweks[k])
	for a in players:
		sent = sock.sendto(game_state.SerializeToString(), a)
	if len(kweks)==3:
		break
'''		


	if data:
		print(address)
		if address not in players:
			#addr = (address,port)
			print("added ",address)
			players.append(address)

		data = data.decode()

		if data == "q":
			break
		received = "DATA: " + data
		print(received)
'''
		for a in players:
			print("sending to",a,":",received)
			sent = sock.sendto(received.encode(), a)	

		'''
		#sent = sock.sendto(data, address)
		# print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)


sock.close()