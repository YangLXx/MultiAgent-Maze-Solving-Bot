
import time
import random
import sys
from tkinter import *
master = Tk()


Width = 80
(x, y) = (7, 7)
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*Width, height=y*Width)
player = (0, y-1)
ma_player = (0, y-1)
score = 1
ma_score = 1
restart = False
ma_restart = False
start_time = 0.0

walk_reward = -0.1

wall_count = 5
walli = 0
walls_gui = []
dynamic_walls = {0:[(1, 1), (2, 2), (3,0), (4,2), (6,3),(3,4), (4,5)], 
                 4:[(0, 4), (0, 5), (2,6), (4,5), (3,4),(1,3), (2,3), (6,2), (5,1), (4,1), (3,1)],
                 2:[(4, 0), (6,2), (3,3),(3,1), (3,2), (2,6), (1,5), (1,4), (1,3)],
                 5:[(4, 0), (5,5), (1,2), (6,2), (5,4), (4,3),(3,1), (3,2), (2,6), (1,5), (1,4), (1,3)],
                 3:[(0, 2), (0, 3), (1, 3), (2,3), (3,1), (4,1), (1,5), (2,5), (5,1), (6,2), (3,3)],
                 1:[(1, 1), (2, 2), (5,0), (4,2), (5,3),(3,3), (6,3)]}

walls = dynamic_walls[walli]
specials = [(6, 0, "red", 30)]

#Toggle agents visibility
show_ma = True
show_solver = True

#counts
tile = 0
total_move = 0


def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        w=board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)
        walls_gui.append(w)

render_grid()

def env_change():
    global walls, walls_gui, walli,start_time,restart,total_move
    for gui in walls_gui :
        board.delete(gui)

    #walli = random.randint(0,wall_count)
    if(walli == wall_count):
        print("CYCLE COMPLETE!!!")
        sys.exit(0)
    else :
        walli += 1 
    walls =  dynamic_walls[walli]
    print("/n CHANGE MAZE ",walli)
    start_time = time.time()
    for (i, j) in walls:
        w=board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)
        walls_gui.append(w)   
    total_move = 0
    restart = True
    ma_restart =True


def try_move(dx, dy):
    global player, x, y, score, walk_reward, agent, restart, tile,total_move
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        if(show_solver):
         board.coords(agent, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_x, new_y)
        tile += 1
        total_move += 1
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            # if score > 0:
            print("Goal! : ", score , " move : ", tile, " tot_mov :",total_move,(" time : %s sec--" % (time.time() - start_time)))
           # else:
            #    print "Goal! : ", score
            restart = True
            return
    #print "score: ", score


def ma_try_move(dx, dy):
    global ma_player, x, y, ma_score, walk_reward, ma_agent, ma_restart
    if ma_restart == True:
        ma_restart_game()
    new_x = ma_player[0] + dx
    new_y = ma_player[1] + dy
    ma_score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        if(show_ma):
            board.coords(ma_agent, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        ma_player = (new_x, new_y)
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            ma_score -= walk_reward
            ma_score += w
            '''if ma_score > 0:
                print "2nd agent Goal! : ", ma_score'''
           # else:
            #    print "Goal! : ", score
            ma_restart = True
            return
    #print "score: ", score    


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)

def ma_restart_game():
    global ma_player, ma_score, ma_agent, ma_restart
    ma_player = (0, y-1)
    ma_score = 1
    ma_restart = False
    if(show_ma):
        board.coords(ma_agent, ma_player[0]*Width+Width*2/10, ma_player[1]*Width+Width*2/10, ma_player[0]*Width+Width*8/10, ma_player[1]*Width+Width*8/10)

def restart_game():
    global player, score, agent, restart, tile
    player = (0, y-1)
    score = 1
    restart = False
    tile = 0
    if(show_solver):
     board.coords(agent, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

def has_restarted():
    return restart

def ma_has_restarted():
    return ma_restart    

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

if(show_solver) :
    agent = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="yellow", width=1, tag="agent")

if(show_ma):
    ma_agent = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="blue", width=1, tag="agent")

board.grid(row=0, column=0)




def start_game():
    global start_time
    start_time = time.time()
    master.mainloop()