
import Gui
import threading
import time
import csv
import pickle
import os
import sys
import signal

discount = 0.8
actions = Gui.actions
states = []
Q = {}
speed_ctrl = 0.02
start_time = 0.0

temp = 0
prev = 1
count = 0

for i in range(Gui.x):
	for j in range(Gui.y):
		states.append((i, j))


def init_Q() :
	for state in states:
		temp = {}
		for action in actions:
			temp[action] = 0.1
		Q[state] = temp

#Read Q
if os.path.isfile('data.pkl'):
	pkl_file = open('data.pkl', 'rb')
	Q = pickle.load(pkl_file) 
	#print Q[(0,4)] 
	print("READ\n")
else :
	init_Q()
	print("Initialize\n")

for wall in Gui.walls:
	temp = {}
	for action in actions:
		temp[action] = -1
	Q[wall] = temp  

for (i, j, c, w) in Gui.specials:
	for action in actions:
		Q[(i, j)][action] = w
		


def do_action(action):
	s = Gui.player
	r = -Gui.score
	if action == actions[0]:
		Gui.try_move(0, -1)
	elif action == actions[1]:
		Gui.try_move(0, 1)
	elif action == actions[2]:
		Gui.try_move(-1, 0)
	elif action == actions[3]:
		Gui.try_move(1, 0)
	else:
		return
	s2 = Gui.player
	r += Gui.score
	return s, action, r, s2

def wall_change():
	global actions,Q
	for wall in Gui.walls:
			temp = {}
			for action in actions:
				temp[action] = 15
			Q[wall] = temp 

#Find Optimal action for a state
def max_Q(s):
	val = None
	act = None
	for a, q in Q[s].items():
		if val is None or (q > val):
			val = q
			act = a
	return act, val


def inc_Q(s, a, alpha, inc):
	Q[s][a] *= 1 - alpha
	Q[s][a] += alpha * inc
	
	
def printq():
	pkl_file = open('data.pkl', 'wb+')
	pickle.dump(Q, pkl_file)
	target = open('dict_2.csv', 'wb')
	writer = csv.writer(target)
	for i in Q.keys():
		writer.writerow([i,Q[i]])
	target.close()
	
def env_change():
	global count
	'''while True:
		time.sleep(120)'''
	wall_change() 
	count = 0           
	Gui.env_change()
	


def run():
	global discount,speed_ctrl,prev,temp,count
	time.sleep(1)
	alpha = 1
	t = 1
	count = 0
	ff = 0
	while True:
		i = 0
		ff += 1
		# Pick  action
		s = Gui.player
		#print Q[(0,4)] 
		max_act, max_val = max_Q(s)
		(s, a, r, s2) = do_action(max_act)
		
		
		# Update Q
		max_act, max_val = max_Q(s2)
		inc_Q(s, a, alpha, r + discount * max_val)

		#  restarted
		t += 1.0
		if (Gui.has_restarted()):
			count += 1 
			t = 1.0
			print("Iteration = " , count)

			if(temp == 8):
				temp = 0
				env_change()
			if(prev == Gui.score):
				temp += 1
			else:
				temp = 0
			prev = Gui.score	
			Gui.restart_game()
			time.sleep(speed_ctrl)

			'''if count == 2 :
				break'''
			

		# Update the learning rate
		alpha = pow(t, -0.1)

		# SLEEP.
		time.sleep(speed_ctrl)
		

#ctrl+C interrupt handler
def signal_handler(signal, frame):
	#print 'You pressed Ctrl+C!'
	printq()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

'''t_env = threading.Thread(target = env_change)
t_env.daemon = True'''

t = threading.Thread(target=run)
t.daemon = True
t.start()
#t_env.start()
Gui.start_game()
