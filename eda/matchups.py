from preprocessor.utils import determine_matchup
from action.core import load_action


def count_matchup_over_time(gid="0021500582", eid=30):
    action = load_action(gid, eid)
    frames = len(action.coords)

    color_dict = {
        0: 'y',  # center
        1: 'g',  # forward
        2: 'c',  # forward
        3: 'b',  # guard
        4: 'r',  # guard
    }

    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt
    for frame in range(frames):
        matchups = determine_matchup(action, frame, "distance")
        for deff in range(5):
            for off in range(5):
                if matchups[deff][off] == 1:
                    plt.plot([frame], [deff + 1], 's', color=color_dict[off])
                    # defended[off].append(off)
                    # color[off].append(color_dict[deff])
    plt.ylim(0, 6)
    center = mpatches.Patch(color=color_dict[0], label='Center')
    powerf = mpatches.Patch(color=color_dict[1], label='Power Forward')
    smallf = mpatches.Patch(color=color_dict[2], label='Small Forward')
    shootg = mpatches.Patch(color=color_dict[3], label='Shooting Guard')
    pointg = mpatches.Patch(color=color_dict[4], label='Point Guard')
    # plt.legend(handles=[center, powerf, smallf, shootg, pointg])
    plt.show()
