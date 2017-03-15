# converts moments to videos

# import some libraries
# from __future__ import print_function
from preprocessor.utils import *
from action.core import load_action
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib
matplotlib.use('TKAgg')

mpl.rcParams['font.family'] = ['Bitstream Vera Sans']


def run(eid, gid, act=None):
    # this is what matplotlib's animation will create before drawing the first
    # frame.
    def draw_court(axis):
        import matplotlib.image as mpimg
        # read image. I got this image from gmf05's github.
        img = mpimg.imread('visualizer/nba_court_T.png')
        plt.imshow(img, extent=axis, zorder=0)  # show the image.

    def init():
        for i in range(10):  # set up players
            player_text[i].set_text('')
            ax.add_patch(player_circ[i])
        for i in range(5):
            ax.add_patch(covariates[i])
        ax.add_patch(ball_circ)  # create ball
        ax.axis('off')  # turn off axis
        dx = 5
        plt.xlim([0 - dx, 100 + dx])  # set axis
        plt.ylim([0 - dx, 50 + dx])
        frame_text.set_text('0')
        return (tuple(player_text) + tuple(player_circ) +
                (ball_circ,) + (frame_text,) + tuple(covariates))

    def animate(n):
        for i, ii in enumerate(player_xy[n]):  # loop through all the players
            # change each players xy position
            player_circ[i].center = (ii[1], ii[2])
            # draw the text for each player.
            player_text[i].set_text(str(jerseydict[str(int(ii[0]))]))
            player_text[i].set_x(ii[1])  # set the text x position
            player_text[i].set_y(ii[2])  # set text y position

        for i, ii in enumerate(get_cannonical_position(action, n)):
            covariates[i].center = (ii[0], ii[1])

        # change ball xy position
        ball_circ.center = (ball_xy[n, 0], ball_xy[n, 1])
        # to keep this constant
        ball_circ.radius = 1.1
        frame_text.set_text(str(n))
        frame_text.set_x(10)
        frame_text.set_y(10)
        return (tuple(player_text) + tuple(player_circ) +
                (ball_circ,) + (frame_text,) + tuple(covariates))

    # the order of events does not match up, so we have to use the eventIds.
    # This loop finds the correct event for a given id# .
    action = load_action(gid, eid)
    if act is None:
        moment = action.coords
    else:
        action.coords = act.coords
        moment = act.coords
    players = action.offense + action.defense
    pos = [str(p[1]) for p in players]
    ids = [str(p[0]) for p in players]
    jerseydict = dict(zip(ids, pos))

    ball_xy = np.array([x[0][2:5] for x in moment])
    player_xy = np.array([np.array(x[1:])[:, 1:4] for x in moment])
    #  ==============================ANIMATION=================

    fig = plt.figure(figsize=(15, 7.5))  # create figure object
    ax = plt.gca()  # create axis object

    draw_court([0, 100, 0, 50])  # draw the court
    player_text = range(10)  # create player text vector
    player_circ = range(10)  # create player circle vector
    covariates = range(5)
    # create circle object for ball
    ball_circ = plt.Circle((0, 0), 1.1, color=[1, 0.4, 0])
    for i in range(10):  # create circle object and text object for each player
        # color scheme   home if i < 5 else away
        col = ['w', 'b'] if i < 5 else ['b', 'w']
        player_circ[i] = plt.Circle(
            (0, 0), 2.2, facecolor=col[0], edgecolor='k')  # player circle
        # player jersey  #  (text)
        player_text[i] = ax.text(0, 0, '', color=col[1],
                                 ha='center', va='center')
    for i in range(5):
        covariates[i] = plt.Circle(
            (0, 0), 1.0, facecolor='g', edgecolor='k')  # player circle
    frame_text = ax.annotate('', xy=[10, 10],
                             color='black', ha='center', va='center')

    ani = animation.FuncAnimation(fig, animate,
                                  frames=np.arange(0, np.size(ball_xy, 0)),
                                  init_func=init, blit=False,
                                  interval=5, repeat=False, save_count=0)

    ani.save('Action_%s_%d.mp4' % (gid, eid), dpi=100, fps=25)
    plt.close('all')
