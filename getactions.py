from visualizer.actionvisualizer import run
from segmenter.core import convert_moment_to_action
from visualizer.visualizer import visualize
import json


SPORTVU_PATH = 'data/sportvu/'


zonedefs = {"0021500149": [364, 375, 381, 392, 404],
            "0021500197": [381, 383, 388, 393],
            "0021500270": [411, 415],
            "0021500316": [320, 322, 324, 338, 352, 377, 385, 392, 395,
                           424, 426, 431, 440, 446, 454, 462, 465],
            "0021500350": [389, 393, 409, 417, 441, 446, 450,
                           454, 466, 484, 486, 496, 520, 523, 526],
            "0021500428": [339, 394, 409, 411, 414, 428, 430,
                           441, 443, 500, 502],
            "0021500476": [278, 346],
            "0021500582": [4, 7, 20, 26, 30, 71, 79, 110, 120,
                           138, 328, 343, 346, 364, 407, 411, 510],
            }


mandefs = {"0021500149": [33, 90, 97, 137, 157, 188, 200, 205, 206,
                          215, 269, 279, 294, 328, 342, 382, 396, 434,
                          475, 477, 500, 540, 550, 555],
           "0021500197": [],
           "0021500270": [422, 426, 427, 477, 496, 514, 556],
           "0021500316": [22, 136, 139, 141, 169, 176, 190, 254, 257,
                          264, 381, 411, 420, 425, 443],
           "0021500350": [485],
           "0021500428": [24, 60, 65, 86, 100, 103, 130, 167, 179, 264,
                          278, 281, 305, 306, 328, 341, 499, 520],
           "0021500476": [2, 9, 16, 26, 27, 36, 51, 62, 85, 86, 107, 109,
                          124, 143, 312, 329, 377, 411, 453, 490, 505],
           "0021500582": [106, 118, 141, 153, 312, 452, 457, 503,
                          525, 541, 543, 577]
           }

"""
length = 0
for key in zonedefs.keys():
    length += len(zonedefs[key] + mandefs[key])

print "LENGTH " + str(length)
"""

"""
print str("*" * 30) + " ZONE DEFENSE " + str("*" * 30)
gid = "0021500197"
with open(SPORTVU_PATH + gid + '.json') as sportvu:
    data = json.load(sportvu)
    eid = 383
    # try:
    action = convert_moment_to_action(data, eid, check_frames=False)
    action.label = -1
    action.save()
    run(eid=eid, gid=gid, act=action)
    except Exception:
        print "gid: " + str(gid) + " | eid: " + str(eid)
"""


print str("*" * 30) + " ZONE DEFENSE " + str("*" * 30)
for gid in sorted(zonedefs.keys()):
    with open(SPORTVU_PATH + str(gid) + '.json') as sportvu:
        data = json.load(sportvu)
    for eid in zonedefs[gid]:
        try:
            action = convert_moment_to_action(data, eid, check_frames=False)
            action.label = -1
            action.save()
            run(eid=eid, gid=gid, act=action)
        except Exception:
            print "gid: " + str(gid) + " | eid: " + str(eid)


print str("*" * 30) + " MAN TO MAN " + str("*" * 30)
for gid in sorted(mandefs.keys()):
    with open(SPORTVU_PATH + str(gid) + '.json') as sportvu:
        data = json.load(sportvu)
    for eid in mandefs[gid]:
        try:
            action = convert_moment_to_action(data, eid, check_frames=False)
            action.label = 1
            action.save()
            run(eid=eid, gid=gid, act=action)
        except Exception:
            print "gid: " + str(gid) + " | eid: " + str(eid)

"""
for gid in sorted(mandefs.keys()):
    with open(SPORTVU_PATH + str(gid) + '.json') as sportvu:
        data = json.load(sportvu)
    for eid in (mandefs[gid] + zonedefs[gid]):
        try:
            visualize(gid, eid, -1 if eid in zonedefs[gid] else 1)
            print "DONE: " + str(gid) + " " + str(eid)
        except Exception:
            print " gid: " + str(gid) + " | eid: " + str(eid)
"""


"""
actions = []
for g in games:
    data = json.load(open("data/actions/" + g + ".json"))
    zoneactions = [key for key in data.keys() if data[key]["label"] == -1]
    print g + " " + str(len(zoneactions))
    actions += zoneactions
    # for key in data.keys():
    #    if data[key]["label"] == 0:
    #        data.pop(key, None)

print "zone defenses: " + str(len(actions))
"""
