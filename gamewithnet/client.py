import socket
import sys

host = "192.168.100.17"
port = 5001
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (host,port)
#message = 'This is the message.  It will be repeated.'
message = "q"
try:

    # Send data
    #print >>sys.stderr, 'sending "%s"' % message
    sent = sock.sendto(message.encode(), server_address)

    # Receive response
    #print >>sys.stderr, 'waiting to receive'
    #data, server = sock.recvfrom(4096)
    #print >>sys.stderr, 'received "%s"' % data

finally:
    #print >>sys.stderr, 'closing socket'
    sock.close()