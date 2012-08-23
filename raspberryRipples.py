import piface.pfion as pfion
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
opponents_number_of_players = list()

pressed_button = 0


def end_game(reason):
	if reason == 0:
		pass
	elif reason ==1:
		print "Game ended due to invalid command line arguments"
	elif reason == 2:
		print "Game ended due to disagreement between players"
	elif reason == 3:
		pass
	exit()

def send_message(code, text):
	global players_ips
	global sock
	MESSAGE= str(code) + "*" + str(text)

	#print "UDP target IP:", REMOTE_UDP_IP
	#print "UDP target port:", REMOTE_UDP_PORT
	print "message sent:", MESSAGE
	p = pfion.PfionPacket()


	for player_ip in players_ips:
		p.data = MESSAGE
		pfion.send_packet(p,player_ip)




def arcade_buttons():
	while(True):
		pfio.write_output(pfio.read_input())


def piface_listener():
	global pressed_button
	while(True):
		pressed_button = pfio.read_input()


def network_listener():
	global opponents_numbers
	global players_times
	global players_scores
	global opponents_number_of_players
	global players_ips
	


	pfion.start_pfio_server(callback=deal_with_packet)
"""
	while(True):
		data, addr = sock2.recvfrom(1024)
"""

def deal_with_packet(packet,sender):
		tu = packet.data.partition("*")

		code = int(tu[0])
		message = tu[2]
		print "%s from %s" %(tu, sender)

		if code == 0:	# players numbers
			opponents_numbers.append(int(message))

		elif code == 1:		# players reaction times
			players_times.append(int(message))

		elif code == 2:		#players scores
			players_scores[players_ips.index(addr)]= int(message)

		elif code == 3:
			print "player number added"
			opponents_number_of_players.append(int(message))
		elif code == 4:
			pass



network_listener_thread = threading.Thread(target=network_listener)
network_listener_thread.daemon = True
network_listener_thread.start()



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



arcade_buttons_thread = threading.Thread(target=arcade_buttons)
arcade_buttons_thread.daemon = True
arcade_buttons_thread.start()

time.sleep(6)

send_message(3,number_of_players)
print "0"

while(len(opponents_number_of_players) < number_of_players-1):
	print opponents_number_of_players
	time.sleep(4)
print "1"
for opponents_number_belief in opponents_number_of_players:
	if opponents_number_belief != number_of_players:
		end_game(2)

print "2"

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

previous_pressed_button = 0
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
					score += 3
					break


#				else:
#					score -1  send score
#					time = -1 send time to other players
#					continue (stay in network waiting mode, but break this interation)

			else:
				received_button = 0
				score -= 1
				send_message(2, -1) # code 2 reaction time, -1 for incorrect answer

