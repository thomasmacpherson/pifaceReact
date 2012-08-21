


# record number of players and their IP address
# specify what player number you are, tell the other machines
#  if 2 machines specify the same player number then exit and tell everyone else to exit.

# start piface input thread
# start network listening thread


# player 1 is sent to a piface input waiting mode

# while loop handles piface input from shared variables
#  if button pressed send number to other players
#    go into network waiting mode


# while network waiting mode:
#   if message received:
#	if button press received:
#		ripple button record time

#		while no piface input:
#			if button press:
#				if button press == button received
#					current time - recorded time
#					send time to other players
#				else:
#					score -1  send score
#					time = -1 send time to other players
#					continue (stay in network waiting mode, but break this interation)

#				while time not received from other players:
#					if received:
#						if your time < their time:
#							leave network waiting mode
#						else: 
#							continue (stay in network waiting mode, but break this interation)

