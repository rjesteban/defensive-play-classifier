from fastdtw import fastdtw
from preprocessor.utils import (determine_matchup_over_time, get_distance,
                                get_coords, get_canonical_position,
                                determine_matchup, arrange_by_position)
from preprocessor.voronoi import get_voronoi_areas
from scipy.spatial.distance import euclidean
import math
import numpy as np


distance = np.zeros((5, 5), dtype=np.int)


def get_entropy(action):
    """
    Gets the entropy of each defender
    Parameters
    ----------
    action : Action instance
    Returns
    ----------
    entropy : list of entropy
    """
    entropy = sum(determine_matchup_over_time(action))  # [25:-25])
    length = len(action.coords)  # [25:-25])
    for r in range(len(entropy)):  # defenders
        for c in range(len(entropy[0])):  # offenders
            if entropy[r][c] > 0:
                p = entropy[r][c] / float(length)
                entropy[r][c] = -(p * math.log(p, 2))
    return [sum(row) for row in entropy]


def get_DTW(action):
    """
    Gets the distance of each defender from its offender via DTW
    Parameters
    ----------
    action : Action instance
    Returns
    ----------
    distances : list of distance based on DTW
    """
    matchup = determine_matchup_over_time(action)
    initial_matchup = [p.argmax() for p in matchup[25]]
    defs = [[] for r in range(5)]
    offs = [[] for r in range(5)]
    for player_index in range(5):
        defs[player_index] = ([get_coords(action.coords[time],
                              action.defense)[player_index][0]
                              for time in range(len(matchup[25:-50]))])
        offs[player_index] = ([get_canonical_position(action,
                              time)[initial_matchup[player_index]]
                              for time in range(len(matchup[25:-50]))])
    return ([fastdtw(np.array(offs[p]), np.array(defs[p]), dist=euclidean)[0]
            for p in range(5)])


def get_mean_distance(action):
    """
    Gets the mean distance of each defender from its offender
    Parameters
    ----------
    action : Action instance
    Returns
    ----------
    mean_distance : list of mean distance
    """
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


def get_mean_distance_from_canonical_position(action):
    """
    Gets the mean distance of each defender from its cannonical position
    Parameters
    ----------
    action : Action instance
    Returns
    ----------
    entropy : list of mean distance from canonical position
    """
    matchup = determine_matchup_over_time(action)
    length = len(matchup)
    match = [p.argmax() for p in matchup[25]]  # sum(matchup)
    dist = [0 for r in range(5)]
    for time in range(len(matchup)):
        defenders = get_coords(action.coords[time], action.defense)
        canon = get_canonical_position(action, time)
        for d in range(5):  # defenders
            dist[d] += get_distance(defenders[d], canon[match[d]])
    return [float(p) / length for p in dist]


def get_time_defending(action):
    """
    Gets the time a defender defends its matchup at frame 25
    Parameters
    ----------
    action : Action instance
    Returns
    ----------
    time : list of time defending (frame based)
    """
    matchup = determine_matchup_over_time(action)
    match = [p.argmax() for p in matchup[25]]  # sum(matchup)
    defending = get_mean_distance_from_canonical_position(action)
    return [float(defending[d] *
            float(sum(matchup[25:-25])[index][d] / len(matchup)))
            for index, d in enumerate(match)]


def get_number_passes(action):
    raise Exception("Passes: Not yet Implemented")


def get_distance_from_post(action):
    length = len(action.coords)
    arrange_by_position(action)
    defenders = [get_coords(action.coords[time], action.defense)
                 for time in range(length)][0:-25]
    post = defenders[0]
    dist_from_post = [0 for r in range(5)]
    for coords in defenders:
        for d in range(5):
            dist_from_post[d] += get_distance(coords[d], post[d])
    return [float(p) / len(defenders) for p in dist_from_post]


def get_diff_canon_vs_matchup(action):
    matchup = determine_matchup_over_time(action)
    length = len(matchup)
    match = [p.argmax() for p in matchup[25]]  # sum(matchup)
    dist = [0 for r in range(5)]
    for time in range(len(matchup)):
        defenders = get_coords(action.coords[time], action.defense)
        canon = get_canonical_position(action, time)
        offenders = get_coords(action.coords[time], action.offense)
        for d in range(5):  # defenders
            dist[d] += (get_distance(defenders[d], offenders[match[d]]) -
                        get_distance(canon[match[d]], offenders[match[d]]))
    return [float(p) / length for p in dist]


# average speed = distance moved / time taken
def get_average_speed_defense(action):
    length = len(action.coords)
    arrange_by_position(action)
    defenders = [get_coords(action.coords[time], action.defense)
                 for time in range(length)][0:-25]
    dist = [0 for r in range(5)]
    for index, coords in enumerate(defenders):
        for d in range(5):
            dist[d] += get_distance(coords[d], defenders[index - 1][d])
    return [float(p) / len(defenders) for p in dist]


# average speed = distance moved / time taken
def get_average_speed_offense(action):
    length = len(action.coords)
    arrange_by_position(action)
    offenders = [get_coords(action.coords[time], action.offense)
                 for time in range(length)][0:-25]
    dist = [0 for r in range(5)]
    for index, coords in enumerate(offenders):
        for d in range(5):
            dist[d] += get_distance(coords[d], offenders[index - 1][d])
    return [float(p) / len(offenders) for p in dist]


def get_excess_voronoi_area(action):
    length = len(action.coords)
    arrange_by_position(action)
    defenders = [get_coords(action.coords[time], action.defense)
                 for time in range(length)][25:-25]
    ref_areas = get_voronoi_areas(defenders[0])
    avg_areas = [0 for r in range(5)]
    for points in defenders:
        areas = get_voronoi_areas(points)
        for i in range(5):
            avg_areas[i] += areas[i]

    return ([ref_areas[p] - (avg / len(defenders))
            for p, avg in enumerate(avg_areas)])
