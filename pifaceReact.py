# pi reaction game


import socket
import sys
import threading
import piface.pfio as pfio
pfio.init()

yourTurn = True
in_play = True

previous = 0




def send_message():
	



def listener(player_number):
	global addr

	if player_number:
		global data1
		while True:
			data1, addr = players[0].recvfrom(1024) 
			print "Lines received from player 1 %s" %data			
				
	else:
		while True:
		global data2
			data2, addr = players[1].recvfrom(1024)
			print "Lines received from player 2 %s" %data	







players = list()

if len(sys.argv) != 1:
	YOUR_IP =socket.gethostbyname(socket.gethostname())
	YOUR_PORT = 5005
	

	if sys.argv[1] == "1":
		PLAYER1_IP="192.168.1.2"  # default IP address for quick play
	else:
		PLAYER1_IP = sys.argv[1]
	PLAYER1_PORT = 4052
	sock1 = socket.socket(socket.AF_INET,
				socket.SOCK_DGRAM)
	sock1.bind((PLAYER1_IP,PLAYER1_PORT))
	players.append(sock1)


	if len(sys.argv) == 3:


		if sys.argv[2] == "1":
			PLAYER2_IP="192.168.0.1" # default IP address for quick play
		else:
			PLAYER2_IP = sys.argv[2]

		PLAYER2_PORT = 4053
		sock2 = socket.socket(socket.AF_INET,
				socket.SOCK_DGRAM)
		sock2.bind((PLAYER2_IP,PLAYER2_PORT))
		players.append(sock2)
		
	if len(players):
		listener_thread_1 = threading.Thread(target=listener, args=(True,))
		listener_thread_1.daemon = True
		listener_thread_1.start()
	if len(players) >1:
		listener_thread_2 = threading.Thread(target=listener, args=(False,))
		listener_thread_2.daemon = True
		listener_thread_2.start()


	while in_play:

		while yourTurn:
			new = pfio.read_input()
			if previous != new:
				previous = new
				send_message(new)
				break

		while not yourTurn:
			if received:
				for player in players:
