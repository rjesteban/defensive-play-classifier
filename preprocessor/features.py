from fastdtw import fastdtw
from preprocessor.utils import (determine_matchup_over_time, get_distance,
                                get_coords, get_cannonical_position,
                                determine_matchup)
from scipy.spatial.distance import euclidean
import math
import numpy as np


distance = np.zeros((5, 5), dtype=np.int)


# entropy for each defender
def get_entropy(action):
    entropy = sum(determine_matchup_over_time(action)[25:-25])
    length = len(action.coords[25:-25])
    for r in range(len(entropy)):  # defenders
        for c in range(len(entropy[0])):  # offenders
            if entropy[r][c] > 0:
                p = entropy[r][c] / float(length)
                entropy[r][c] = -(p * math.log(p, 2))
    return [sum(row) for row in entropy]

"""
# entropy for each defender
def get_entropy(action):
    entropy = []
    length = len(action.coords)
    for i in range(length):
        entropy.append(determine_matchup(action, i, "canonical"))

    entropy = sum(entropy)
    for r in range(len(entropy)):  # defenders
        for c in range(len(entropy[0])):  # offenders
            if entropy[r][c] > 0:
                p = entropy[r][c] / float(length)
                entropy[r][c] = -(p * math.log(p, 2))
    return [sum(row) for row in entropy]
"""


def get_DTW(action):
    matchup = determine_matchup_over_time(action)
    length = len(matchup)
    initial_matchup = [p.argmax() for p in matchup[25]]
    defs = [[] for r in range(5)]
    offs = [[] for r in range(5)]
    for player_index in range(5):
        defs[player_index] = ([get_coords(action.coords[time],
                              action.defense)[player_index][0]
                              for time in range(len(matchup[25:-50]))])
        offs[player_index] = ([get_coords(action.coords[time],
                              action.offense)[initial_matchup[player_index]]
                              for time in range(len(matchup[25:-50]))])
    return ([fastdtw(np.array(offs[p]), np.array(defs[p]), dist=euclidean)[0]
            for p in range(5)])


def get_mean_distance(action):
    matchup = determine_matchup_over_time(action)
    length = len(matchup)
    match = [p.argmax() for p in matchup[25]]  # not sum(matchup)
    dist = [0 for row in range(5)]
    for time in range(len(matchup)):
        defenders = get_coords(action.coords[time], action.defense)
        offenders = get_coords(action.coords[time], action.offense)
        for d in range(5):  # defenders
            dist[d] += get_distance(defenders[d], offenders[match[d]])
    return [float(p) / length for p in dist]


def get_mean_distance_from_cannonical_position(action):
    matchup = determine_matchup_over_time(action)
    length = len(matchup)
    match = [p.argmax() for p in matchup[25]]  # sum(matchup)
    dist = [0 for r in range(5)]
    for time in range(len(matchup)):
        defenders = get_coords(action.coords[time], action.defense)
        # offenders = get_coords(action.coords[time], action.offense)
        offenders = get_cannonical_position(action, time)
        for d in range(5):  # defenders
            dist[d] += get_distance(defenders[d], offenders[match[d]])
    return [float(p) / length for p in dist]


def get_number_passes(action):
    raise Exception("Passes: Not yet Implemented")


"""
import numpy as np
from scipy.spatial.distance import euclidean

from fastdtw import fastdtw

x = np.array([[1,1], [2,2], [3,3], [4,4], [5,5]])
y = np.array([[2,2], [3,3], [4,4]])
distance, path = fastdtw(x, y, dist=euclidean)
print(distance)
"""
