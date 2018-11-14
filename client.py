#Credits to Mellark Channel in Youtube for the chat_server_client tutorial
import socket, select, string, sys

def prompt():
    sys.stdout.write('<You> ') #Ask name
    sys.stdout.flush() #make sure that empty to not input garbage

if __name__ == " __main__ ":
    if(len(sys.argv) < 3):
        print("Use the command: python3 client.py <hostname> <port>")
        sys.exit()

    host = sys.argv[1] # the host is the first argument
    port = int(sys.argv[2]) #2nd argument

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #AF_INET means IP version 4
    #SOCK_STREAM denotes that we are using TCP
    s.settimeout(2) #if server not found then close  

    try:
        s.connect(((host,port)))
    except:
        print("Unable to connect to server")
        sys.exit()
    
    print("Connected to server. You may now type.")
    prompt()

    while 1: #while true
        socket_list=[sys.stdin,s]
        
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], []) # socket list and 2 empty arrays as parameters
        for sock in read_sockets:
            if sock == s:
                data = sock.recv(4096) #can get data upto 4 kilobytes
                if not data:
                    print("DISCONNECTED from Server")
                    sys.exit()
                else:
                    sys = stdout.write(data.decode())
                    prompt()
            else:
                msg = sys.stdin.readline()
                s.send(msg)
                prompt()



