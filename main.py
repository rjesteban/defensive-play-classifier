from segmenter.core import pick_possessions
from random import randint
from playbyplay.utils import acquire_pbp_json

if __name__ == '__main__':
    ids = ['0021500316', '0021500270', '0021500149', '0021500197',
           '0021500428', '0021500350', '0021500476', '0021500582']
    moments = {"0021500316": [],
               "0021500270": [],
               "0021500149": [],
               "0021500197": [],
               "0021500428": [],
               "0021500350": [],
               "0021500476": [],
               "0021500582": []
               }

    games = {"0021500149": [33, 46, 83, 88, 90, 97, 137, 157, 188, 200, 205,
                            206, 215, 269, 279, 294, 302, 328, 342, 364, 371,
                            382, 394, 396, 434, 456, 475, 477, 500, 540,
                            550, 552],
             "0021500197": [2, 7, 10, 34, 39, 56, 68, 78, 87, 89, 101, 128,
                            131, 174, 184, 199, 201, 224, 235, 290,
                            336, 374, 394, 398, 436, 443, 456, 458, 467,
                            471, 472, 482, 499],
             "0021500270": [9, 26, 40, 111, 116, 127, 164, 172, 194, 227, 236,
                            244, 295, 306, 311, 317, 324, 351, 355, 372, 422,
                            426, 427, 449, 477, 479, 496, 514, 556, 564,
                            565, 567, 595],
             "0021500316": [22, 48, 66, 73, 82, 114, 121, 123, 136, 139, 141,
                            145, 169, 176, 190, 201, 249, 254, 257, 264,
                            296, 324, 326, 381, 411, 420, 425, 443],
             "0021500350": [8, 14, 17, 21, 29, 46, 55, 141, 169, 176, 191, 225,
                            250, 292, 305, 319, 324, 370, 421, 429, 444,
                            450, 485, 512, 536],
             "0021500428": [12, 24, 60, 65, 86, 99, 100, 103, 130, 137, 167,
                            179, 244, 257, 264, 278, 281, 305, 306, 328,
                            330, 341, 388, 395, 456, 499, 520],
             "0021500476": [2, 9, 16, 26, 27, 36, 41, 51, 62, 69, 85, 86, 94,
                            107, 109, 124, 141, 143, 163, 189, 235, 241, 255,
                            265, 312, 329, 332, 377, 383, 411, 453, 490, 505],
             "0021500582": [106, 118, 141, 149, 153, 188, 280, 312, 452, 457,
                            503, 525, 528, 541, 543, 551, 562, 572, 574, 577]
             }

    print "games = {"
    for gid in moments.keys():
        for id in ids:
            evts = [evt for evt in pick_possessions(gid)
                    if evt not in games[gid]]
            moments[gid] = [evts[randint(0, len(evts) - 1)]
                            for index in range(25)]
        print '    "' + gid + '": ' + str(sorted([evt for evt in moments[gid]
                                          if evt not in games[gid]])) + ", "
    print "}"

    """
    import json
    from segmenter.core import convert_moment_to_action
    testdata = json.load(open('data/sportvu/0021500582.json'))
    eid = 139  # 30  # 4
    action = convert_moment_to_action(testdata, eid)
    print action
    from visualizer.actionvisualizer import run
    run(eid=eid, act=action)
    """

    """
    from action.core import load_action
    from preprocessor.utils import determine_matchup
    from frameone import run as fr_run
    eid = 139
    action = load_action("0021500582", eid)

    from preprocessor.features import get_entropy, get_mean_distance
    import numpy as np
    entropy = get_entropy(action)

    print "event id: " + str(eid)
    print "avg entropy: " + str(np.mean(entropy))
    print entropy

    mean_dist = get_mean_distance(action)
    print "avg dist: " + str(np.mean(mean_dist))
    print mean_dist

    # fr_run(eid=eid)
    # """
