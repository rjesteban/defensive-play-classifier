from preprocessor.utils import determine_matchup, get_distance, get_coords
import math
import numpy as np


distance = np.zeros((5, 5), dtype=np.int)


# entropy for each defender
def get_entropy(action):
    entropy = []
    length = len(action.coords)
    for i in range(length):
        entropy.append(determine_matchup(action, i, "canonical"))

    entropy = sum(entropy)
    indices = [r.argmax() for r in entropy]
    print indices
    for r in range(len(entropy)):  # defenders
        for c in range(len(entropy[0])):  # offenders
            if entropy[r][c] > 0:
                p = entropy[r][c] / float(length)
                entropy[r][c] = -(p * math.log(p, 2))
    return [sum(row) for row in entropy]


def get_mean_distance(action):
    matchup = []
    length = len(action.coords)
    for i in range(length):
        matchup.append(determine_matchup(action, i, "canonical"))

    match = [p.argmax() for p in sum(matchup)]
    dist = range(5)
    for time in range(length):
        defenders = get_coords(action.coords[time], action.defense)
        offenders = get_coords(action.coords[time], action.offense)
        for d in range(5):  # defenders
            dist[d] += get_distance(defenders[d], offenders[match[d]])
    return [float(p) / length for p in dist]


def get_number_passes(action):
    raise Exception("Passes: Not yet Implemented")
