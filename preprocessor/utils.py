import math
import numpy as np


def determine_matchup_over_time(action):
    matchup = []
    length = len(action.coords)
    for i in range(length):
        matchup.append(determine_matchup(action, i, "canonical"))
    return matchup


def get_distance(p1, p2):
    sidex = math.fabs(p1[0] - p2[0])
    sidey = math.fabs(p1[1] - p2[1])
    return math.fabs(math.sqrt(sidex ** 2 + sidey ** 2))


def transform_wlog(action):
    coordinates = []
    for entity in action.coords:
        for e in entity:
            x = e[2]
            y = e[3]
            if x > 47:
                e[2] = round(94 - x, 4)
            else:
                e[3] = round(50 - y, 4)
        coordinates.append(entity)
    action.coords = coordinates
    return action


def arrange_by_position(action):
    rank = {'C': 0, 'C-F': 1, 'F-C': 2, 'F': 3, 'F-G': 4, 'G-F': 5, 'G': 6}
    offense = range(len(action.offense))
    for i in range(len(action.offense)):
        j = i
        key = rank[action.offense[i][1]]
        while j > 0 and rank[str(offense[j - 1][1])] > key:
            offense[j] = offense[j - 1]
            j -= 1
        offense[j] = action.offense[i]

    defense = range(len(action.defense))
    for i in range(len(action.defense)):
        j = i
        key = rank[action.defense[i][1]]
        while j > 0 and rank[str(defense[j - 1][1])] > key:
            defense[j] = defense[j - 1]
            j -= 1
        defense[j] = action.defense[i]
    action.offense = offense
    action.defense = defense
    return action


def get_coords(coords, players):
    ctk = []
    for p in players:
        for coord in coords:
            pid = coord[1]
            if str(pid) == str(p[0]):
                ctk.append([coord[2], coord[3]])
    return ctk


def get_canonical_position(action, time):
    arrange_by_position(action)
    ball = (action.coords[time][0][2], action.coords[time][0][3])
    otk = get_coords(action.coords[time], action.offense)
    hoop = (4.0, 25.0)
    pos = []
    for o in otk:
        xpos = (0.62 * o[0]) + (0.11 * ball[0]) + (0.27 * hoop[0])
        ypos = (0.62 * o[1]) + (0.11 * ball[1]) + (0.27 * hoop[1])
        pos.append([xpos, ypos])
    return pos


def determine_matchup(action, time, by):
    matrix = np.zeros((5, 5), dtype=np.float32)
    arrange_by_position(action)
    defenders = get_coords(action.coords[time], action.defense)
    if by == "distance":
        offender_loc = get_coords(action.coords[time], action.offense)
    else:
        offender_loc = get_canonical_position(action, time)

    # defender rows
    # offender cols
    for i, (px, py) in enumerate(defenders):
        a = [get_distance((px, py), (d[0], d[1])) for d in offender_loc]
        matrix[i][a.index(min(a))] = 1
    return matrix
