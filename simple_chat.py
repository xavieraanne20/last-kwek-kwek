import socket
import sys

#ensures to print out error using try-catch-------------------
try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #AF_INET means IP version 4
    #SOCK_STREAM denotes that we are using TCP
except socket.error:
    print("Failed to connect")
    sys.exit()

#-------------------------------------------------------------

#Able to connect successfully---------------------------------
print("Socket created")
host="202.92.144.45"
port=80
s.connect((host,port))
print("Socket Connected " + host + " at port " + str(port) )

#-------------------------------------------------------------

    