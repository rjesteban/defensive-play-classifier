from action.core import *
from preprocessor.utils import get_canonical_position
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def run(eid):
    frame = 0

    action = load_action("0021500582", eid)
    moment = action.coords

    ball_xy = np.array([x[0][2:4] for x in moment][frame])
    player_xy = np.array([np.array(x[1:])[:, 2:4] for x in moment][frame])

    # fig = plt.figure(figsize=(15, 7.5))
    ax = plt.gca()

    img = mpimg.imread('visualizer/nba_half_court_T.png')
    plt.imshow(img, extent=[0, 100, 0, 50], zorder=0)

    player_circ = range(10)
    ball_circ = plt.Circle((ball_xy[0], ball_xy[1]), 1.1,
                           color=[1, 0.4, 0])
    for i in range(10):
        col = ['w', 'b'] if i < 5 else ['b', 'w']
        player_circ[i] = plt.Circle((player_xy[i][0],
                                    player_xy[i][1]),
                                    2.2,
                                    facecolor=col[0], edgecolor='k')

    for i in range(10):
        ax.add_patch(player_circ[i])
    ax.add_patch(ball_circ)
    ax.axis('off')
    dx = 5
    plt.xlim([0 - dx, 100 + dx])
    plt.ylim([0 - dx, 50 + dx])
    pos = get_canonical_position(action, frame, by="canonical")
    plt.plot([p[0] for p in pos], [p[1] for p in pos], 'o', color='g')
    plt.show()
