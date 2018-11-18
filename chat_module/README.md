DIRECTORY:

parent folder
	|-- chat_client.py
	|-- README.md
	|-- tcp_packet_pb2.py
	|==== proto			(subfolder)
			|-- player.proto
			|-- player_pb2.py
			|-- tcp_packet.proto


First Player:
	When the first player connects to the client, he/she must select option [1] to create a new lobbe. The max number of players must be specified.

	The Lobby ID of the newly created lobby will be displayed. The player must now connect to the lobby by choosing option 2 and typing in the lobby id.

Succeeding Players:
	The players must choose option [2] to connect to the lobby created by the first player, using the lobby id created. 

Messages - once connected to a lobby, the player has the ability to send messages to all other players currently in the lobby.

Player List - the player may type "show_players" to  display the list of players currently in the lobby

Quit Chat - if the player wishes to disconnect, he/she must type "exit". All other players in the Lobby will be informed of the event.