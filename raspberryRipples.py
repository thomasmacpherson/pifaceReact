import piface.pfion as pfion
import sys
import threading
import time
import piface.pfio as pfio
import pygame

from pygame.locals import *

pygame.init()
font = pygame.font.Font(None, 60)
big_font = pygame.font.Font(None, 400)

screen=pygame.display.set_mode((1100,900), FULLSCREEN)

background = pygame.image.load("rpibatakbg.png").convert()

scr_pos_x = -50
scr_pos_y = 0

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
received_button = 0

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
		check_keys()



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

def mouse_positioning():
	pos = pygame.mouse.get_pos()
	while(True):
		if pygame.mouse.get_pressed()[0]:
			if pygame.mouse.get_pos() != pos:
				print	pygame.mouse.get_pos()
				pos = pygame.mouse.get_pos()


	
def draw_screen():
	screen.blit(background, (scr_pos_x - 200 ,scr_pos_y - 100))

	display_score = font.render(str(score), 1, (0,0,0))
	screen.blit(display_score, (880 + scr_pos_x, 358 + scr_pos_y))

	for ind, player in enumerate(players_scores):
		screen.blit(font.render("Player " + str(ind+1)+ " has a score of " + str(player), 1, (0,0,0)), (880 + scr_pos_x + (ind * 50), 358 + scr_pos_y))		
	pygame.display.update()


def check_keys():
	for event in pygame.event.get():
		#if event.type == QUIT:
		#	pygame.quit()
		#	sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()		
	#time.sleep(1)
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
			players_times.append(float(message))

		elif code == 2:		#players scores
			print players_ips
			print sender[0]
			players_scores[players_ips.index(sender[0])]= int(message)
			print "your score %d" %score
			print "Opponents' scores %s" %players_scores

		elif code == 3:
			print "player number added"
			opponents_number_of_players.append(int(message))
		elif code == 4:
			global received_button
			received_button = int(message)
			button_ripple(received_button)

def button_ripple(b_number):
	x_pos = 0
	y_pos = 0


	if b_number == 1:
		x_pos = 267
		y_pos = 434

	elif b_number == 2:
		x_pos = 467
		y_pos = 610

	elif b_number == 4:
		x_pos = 536
		y_pos = 435

		
	elif b_number == 8:
		x_pos = 465
		y_pos = 261

		
	elif b_number == 16:
		x_pos = 588
		y_pos = 780

		
	elif b_number == 32:
		x_pos = 735
		y_pos = 432

		
	elif b_number == 64:
		x_pos = 584
		y_pos = 100

		
	elif b_number == 128:
		x_pos = 812
		y_pos = 778

		
	elif b_number == 256:
		x_pos = 878
		y_pos = 637

		
	elif b_number == 512:
		x_pos = 864
		y_pos = 233

		
	elif b_number == 1024:
		x_pos = 796
		y_pos = 100

		
	elif b_number == 2048:
		x_pos = 1095
		y_pos = 565

		
	elif b_number == 4096:
		x_pos = 1095
		y_pos = 311

		
	for i in range(1,10):
		for j in range(1,5):
			pygame.draw.circle(screen, (100,0,20),(x_pos + scr_x_pos, y_pos + scr_y_pos), i*j*10, 4) 
			draw_screen()
			time.sleep(.5)

network_listener_thread = threading.Thread(target=network_listener)
network_listener_thread.daemon = True
network_listener_thread.start()

#mouse_thread = threading.Thread(target=mouse_positioning)
#mouse_thread.daemon = True
#mouse_thread.start()

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

draw_screen_thread = threading.Thread(target=draw_screen)
draw_screen_thread.daemon = True
draw_screen_thread.start()


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
		#print "commander"

		if pressed_button != previous_pressed_button and pressed_button != 0:
			previous_pressed_button = pressed_button
			send_message(4,pressed_button)
			while(len(players_times)!=number_of_players-1):
				if pressed_button != 0 and pressed_button != previous_pressed_button:
					print "only one serve please"
					score -= 1
					send_message(2, score)
				previous_pressed_button = pressed_button
			print "result received"
			if sum(players_times) == (number_of_players-1)*-1: # if no players got the answer wrong
				print "still commander"		# continue commander while loop
			else:
				commander = False
			print sum(players_times)
			print (number_of_players-1)*-1
			del players_times[:]
		previous_pressed_button = pressed_button
	
#TODO : if neither get right button become the commander again

	previous_pressed_button = pressed_button


# while network waiting mode:
#   if message received:
#	if button press received:
#		ripple button record time


	while(not commander):
		previous_pressed_button = pressed_button
		#print "not commander"
		for player in players_times:
			player = -2

		if received_button != 0:
			# ripple button
			received_time = time.time()

#		while no piface input:
#			if button press:
			#count = 100000
			while(True):
				if pressed_button != previous_pressed_button and pressed_button != 0:
					break
				#count -= 1
#				if button press == button received
#					current time - recorded time
#					send time to other players
			print "new button press"

			previous_pressed_button = pressed_button

			if pressed_button == int(received_button): # correct answer
				received_button = 0
				current_time = time.time()
				reaction_time = current_time - received_time
				send_message(1,reaction_time) # code 2 is reaction time
				print "pressed quals received"

#				while time not received from other players:
#					if received:
#						if your time < their time:
#							leave network waiting mode
#						else: 
#							continue (stay in network waiting mode, but break this interation)
				commander = True
				while(len(players_times) > 0):
					wl = True
					for player in players_times:
						if player == -2:
							wl = False
					if wl == True:
						break
					print "4"

				for player in players_times:
					if player == -2:
						continue
					elif player == -1:
						continue
					elif player < reaction_time:
						commander = False

				if(commander):
					score += 3
				else:
					score -= 1

				send_message(2, score)
					


#				else:
#					score -1  send score
#					time = -1 send time to other players
#					continue (stay in network waiting mode, but break this interation)
				print "finished "
			else:
				print received_button
				received_button = 0
				print "pressed not equal to received "
				print pressed_button

				send_message(1, -1) # code 2 reaction time, -1 for incorrect answer
				score -= 1
				send_message(2, score)
			previous_pressed_button = pressed_button
		else:
			if pressed_button != previous_pressed_button and pressed_button != 0:
				score -= 1
				print "not your turn to press"
				send_message(2, score)
			previous_pressed_button = pressed_button
