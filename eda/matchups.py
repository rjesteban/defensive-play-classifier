from preprocessor.utils import determine_matchup
from action.core import load_action


def count_matchup_over_time(gid="0021500582", eid=30):
    action = load_action(gid, eid)
    frames = len(action.coords)

    color_dict = {
        4: 'r',  # guard
        3: 'b',  # guard
        2: 'g',  # forward
        1: 'm',  # forward
        0: 'y'  # center
    }

    # defenders (y axis)
    # 4 guard
    # 3 guard
    # 2 forward
    # 1 forward
    # 0 center

    # time (x axis)

    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt
    for frame in range(frames):
        matchups = determine_matchup(action, frame, "distance")
        for deff in range(5):
            for off in range(5):
                if matchups[deff][off] == 1:
                    plt.plot([frame], [deff], 's', color=color_dict[off])
                    # defended[off].append(off)
                    # color[off].append(color_dict[deff])
    plt.ylim(-0.5, 5.5)
    center = mpatches.Patch(color=color_dict[0], label='Center')
    powerf = mpatches.Patch(color=color_dict[1], label='Power Forward')
    smallf = mpatches.Patch(color=color_dict[2], label='Small Forward')
    shootg = mpatches.Patch(color=color_dict[3], label='Shooting Guard')
    pointg = mpatches.Patch(color=color_dict[4], label='Point Guard')
    # plt.legend(handles=[center, powerf, smallf, shootg, pointg])
    plt.show()
