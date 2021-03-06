
from Tkinter import *
import time
import random
master = Tk()


Width = 80
(x, y) = (7, 7)
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*Width, height=y*Width)
player = (0, y-1)
score = 1
restart = False
walk_reward = -0.1
start_time = 0.0


dynamic_walls = {0:[(1, 1), (2, 2), (3,0), (4,2), (6,3),(3,4), (4,5)], 
                 1:[(0, 4), (0, 5), (2,6), (4,5), (3,4),(1,3), (2,3), (6,2), (5,1), (4,1), (3,1)],
                 2:[(4, 0), (6,2), (3,3),(3,1), (3,2), (2,6), (1,5), (1,4), (1,3)],
                 3:[(4, 0), (5,5), (1,2), (6,2), (5,4), (4,3),(3,1), (3,2), (2,6), (1,5), (1,4), (1,3)],
                 4:[(0, 2), (0, 3), (1, 3), (2,3), (3,1), (4,1), (1,5), (2,5), (5,1), (6,2), (3,3)],
                 5:[(1, 1), (2, 2), (5,0), (4,2), (5,3),(3,3), (6,3)]}

walls = dynamic_walls[2]
specials = [(6, 0, "red", 30)]

tile = 0;



def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

render_grid()





def try_move(dx, dy):
    global player, x, y, score, walk_reward, agent, restart,tile
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(agent, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_x, new_y)
        tile += 1
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            if score > 0:
                print "Goal! : ", score , " move : ", tile,(" time : %s seconds ---" % (time.time() - start_time))
           # else:
            #    print "Goal! : ", score
            restart = True
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


def restart_game():
    global player, score, agent, restart, tile
    player = (0, y-1)
    score = 1
    restart = False
    board.coords(agent, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)
    tile = 0
def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

agent = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="yellow", width=1, tag="agent")

board.grid(row=0, column=0)


def start_game():
    global start_time
    start_time = time.time()
    master.mainloop()
