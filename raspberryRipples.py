import socket
import sys
import threading
import time
import piface.pfio as pfio
pfio.init()

number_of_players = 0
player_number = 0

in_game = True

score = 0

players_ips = list()
players_scores = list()
players_times = list()

opponents_numbers = list()



def send_message(code, text):
	global REMOTE_UDP_IP
	global REMOTE_UDP_PORT
	global sock
	MESSAGE= str(code) += text

	#print "UDP target IP:", REMOTE_UDP_IP
	#print "UDP target port:", REMOTE_UDP_PORT
	print "message sent:", MESSAGE

	sock = socket.socket(socket.AF_INET,
			     socket.SOCK_DGRAM)
	sock.sendto(MESSAGE, (REMOTE_UDP_IP, REMOTE_UDP_PORT))




def arcade_buttons:
	while(True):
		pfio.write_output(pfio.read_input())


def piface_listener():
	while(True):
		pressed_button = pfio.read_input())


def network_listener():
	while(True):
		data, addr = sock2.recvfrom(1024)
		tu = data.partition("*")
		code = tu[0]
		message = tu[2]

		if code == 0:	# players numbers
			opponents_numbers.append(int(message))

		elif code == 1:		# players reaction times
			players_times.append(int(message))

		elif code == 2:		#players scores
			players_scores[players_ips.index(addr)]= int(message)


		elif code == 3:
			pass
		elif code == 4:
			pass







# record number of players and their IP addresses
if len(sys.argv) > 3:
	number_of_players = int(sys.argv[1])
	player_number = int(sys.argv[2])

	if player_number > number_of_players:
		print "Your player number can't be higher than the number of players"
		end_game(1) # end the game with reason (command line error)

	if number_of_players < 2:
		print "This is a multiplayer game, you must have more than one player"
		end_game(1) # end the game with reason (command line error)
	else:
		for i, argument in enumerate(sys.argv):
			if i > 2 :
				players_ips.append(sys.argv[i])
				players_scores.append(0)


	if number_of_players-1 != len(players_ips):
		print "The number of player IPs you have given doesn't match the number of players specified"
		end_game(1) # end the game with reason (command line error)
	
else:
	print "This is a networked game, you must provide IP addresses for opponents"
	exit()


# start piface input thread
# start network listening thread
# start arcade buttons thread (for lighting up buttons when they are pressed)

piface_listener_thread = threading.Thread(target=piface_listener)
piface_listener_thread.daemon = True
piface_listener_thread.start()

network_listener_thread = threading.Thread(target=network_listener)
network_listener_thread.daemon = True
network_listener_thread.start()

arcade_buttons_thread = threading.Thread(target=arcade_buttons)
arcade_buttons_thread.daemon = True
arcade_buttons_thread.start()




#	specify what player number you are, tell the other machines

send_message(0,player_number)


#	wait for players responses

	

while(len(opponents_numbers)<number_of_players-1):
	pass


# 	if 2 machines specify the same player number then exit and tell everyone else to exit.
for opponent_number in opponents_numbers:
	if player_number == opponent_number:
		end_game(2) # end the game with the reason (opponent disagreement)




commander = False	# player 1 is sent to a piface input waiting mode

if player_number == 1:
	commander = True


while(in_game):

# while loop handles piface input from shared variables
#  if button pressed send number to other players
#    go into network waiting mode
	while(commander):
		if pressed_button != previous_pressed_button and pressed_button != 0:
			send_message(1,pressed_button)
			while(len(players_times)!=number_of_players-1):
				pass
			if sum(players_times) != (number_of_players-1)*-1: # if no players got the answer wrong
				break		# break commander while loop
		previous_pressed_button = pressed_button
	
#TODO : if neither get right button become the commander again




# while network waiting mode:
#   if message received:
#	if button press received:
#		ripple button record time


	while(not commander):
		for player in players_times:
			player = -2

		if received_button != 0:
			# ripple button
			received_time = time.time()

#		while no piface input:
#			if button press:
			count = 100000
			while(count):
				if pressed_button != previous_pressed_button and pressed_button != 0:
					break
				count -= 1
#				if button press == button received
#					current time - recorded time
#					send time to other players

			if pressed_button == int(received_button):
				received_button = 0
				current_time = time.time()
				reaction_time = current_time - received_time
				send_message(2,reaction_time) # code 2 is reaction time


#				while time not received from other players:
#					if received:
#						if your time < their time:
#							leave network waiting mode
#						else: 
#							continue (stay in network waiting mode, but break this interation)
				commander = True
				while(True):

					for player in players_times:
						if player == -2:
							continue
						elif player < reaction_time:
							commander = False

					break


#				else:
#					score -1  send score
#					time = -1 send time to other players
#					continue (stay in network waiting mode, but break this interation)

			else:
				received_button = 0
				score -= 1
				send_message(2, -1) # code 2 reaction time, -1 for incorrect answer

