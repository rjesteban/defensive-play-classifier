# converts moments to videos

# import some libraries
# from __future__ import print_function
import matplotlib
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import matplotlib.animation as animation

matplotlib.use('TKAgg')

mpl.rcParams['font.family'] = ['Bitstream Vera Sans']

file_name = "videos/006.mp4.json"
json_data = open('videos/006.mp4.json')
data = json.load(json_data)
length = len(data["o1"])


#  Animation function / loop
def draw_court(axis):
    import matplotlib.image as mpimg
    img = mpimg.imread('nba_court_T.png')
    plt.imshow(img, extent=axis, zorder=0)


def animate(n):
    print "n" * 10, " ", n
    print(player_xy[n][0][1])

    for p, x, y in player_xy[n]:
        
        player_circ[p].center = (x, y)
        player_text[p].set_text(p)
        player_text[p].set_x(x)  # set the text x position
        player_text[p].set_y(y)  # set text y position
    return tuple(player_text)


# this is what matplotlib animation will create before drawing the first frame
def init():
    for i in range(10):  # set up players
        player_text[i].set_text('')
        ax.add_patch(player_circ[i])
    ax.axis('off')  # turn off axis
    dx = 5
    plt.xlim([0 - dx, 100 + dx])  # set axis
    plt.ylim([0 - dx, 50 + dx])
    return tuple(player_text) + tuple(player_circ)


xy = ([data["o" + str(i + 1)] for i in range(5)] +
      [data["d" + str(i + 1)] for i in range(5)])
print len(xy[0])
player_xy = []

for frame in range(len(xy[0])):  # 305
    fr = []
    for p in range(len(xy)):  # 10
        xy[p][frame].insert(0, (p % 5) + 1 )
        fr.append(xy[p][frame])
        print xy[p][frame]
    player_xy.append(fr)

#  =================ANIMATION=================

fig = plt.figure(figsize=(15, 7.5))  # create figure object
ax = plt.gca()  # create axis object

draw_court([0, 100, 0, 50])  # draw the court
player_text = range(10)  # create player text vector
player_circ = range(10)  # create player circle vector
for i in range(10):  # create circle object and text object for each player
    col = ['w', 'r'] if i < 5 else ['r', 'w']  # color scheme
    player_circ[i] = plt.Circle((0, 0), 2.2, facecolor=col[0], edgecolor='k')
    player_text[i] = ax.text(0, 0, '', color=col[1], ha='center', va='center')

ani = animation.FuncAnimation(fig, animate,
                              frames=np.arange(0, length),
                              init_func=init,
                              blit=True,
                              interval=5,
                              repeat=False, save_count=0)
ani.save('Event_%s.mp4' % (file_name), dpi=100, fps=25)
plt.close('all')
