from visualizer.actionvisualizer import run
from segmenter.core import convert_moment_to_action
import json

SPORTVU_PATH = 'data/sportvu/'


zonedefs = {"0021500149": [],
            "0021500197": [],
            "0021500270": [],
            "0021500316": [],
            # "0021500336": [574, 643], REMOVE THIS
            "0021500350": [389, 393, 409, 417, 441, 446, 450,
                           454, 466, 484, 486, 496, 520, 523, 526],
            "0021500428": [339, 394, 409, 411, 414, 428, 430,
                           441, 443, 500, 502],
            "0021500476": [278, 346],
            "0021500582": [4, 7, 20, 26, 30, 71, 79, 110, 120,
                           138, 328, 343, 346, 364, 407, 411, 510],
            "0021500040": [117]
            }

"""
for gid in zonedefs.keys():
    with open(SPORTVU_PATH + gid + '.json') as sportvu:
        data = json.load(sportvu)
    for eid in zonedefs[gid]:
        print "eid being processed: " +  str(eid)
        action = convert_moment_to_action(data, eid, check_frames=False)
        action.label = -1
        action.save()
"""


# gid = "0021500350"
for gid in zonedefs.keys():
    with open(SPORTVU_PATH + str(gid) + '.json') as sportvu:
        data = json.load(sportvu)
    for eid in zonedefs[gid]:
        try:
            action = convert_moment_to_action(data, eid, check_frames=False)
            action.label = -1
            action.save()
            run(eid=eid, gid=gid, act=action)
        except Exception:
            print "gid: " + str(gid) +  " | eid: " + str(eid)
