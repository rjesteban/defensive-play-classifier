from action import Action
from sportvu.utils import get_moment
import json
import math


def time_difference(time1, time2):
    time_1 = [int(i) for i in time1.split(':')]
    time_2 = [int(i) for i in time2.split(':')]
    t1 = (time_1[0] * 60) + time_1[1]
    t2 = (time_2[0] * 60) + time_2[1]
    if t1 < t2:
        raise Exception(time1 + " is less than " + time2)
    return int(math.fabs(t1 - t2))


# time difference quota is still under experiment, EDA needed
def pick_possessions(pbp):
    """
    picks ids of moments ending in a shot, or a steal.
    do not pick moments where the previous moment was a steal.
    pick after timeout/violation/substitution/foul moments.

    Keyword argument:
    pbp -- file name (str)

    returns:
        array of gameid, eventid
    """
    data = json.load(open(pbp))
    row_set = data['resultSets'][0]['rowSet']
    moments = []

    for i in range(1, len(row_set)):
        shot_attempt = (1 <= row_set[i][2] <= 2)
        turnover = row_set[i][2] == 5
        stop_play = row_set[i][2] in [7, 9] and row_set[i - 1][2] not in [7, 9]
        came_from_steal = (row_set[i - 1][2] == 5 and
                           row_set[i - 1][3] <= 2 and
                           time_difference(row_set[i - 1][6],
                           row_set[i][6]) < 5)
        follow_up = (row_set[i - 1][2] == 4 and
                     time_difference(row_set[i - 1][6], row_set[i][6]) < 5)
        attempt = (shot_attempt and not follow_up) or turnover or stop_play
        if attempt and not came_from_steal:
            moments.append(row_set[i][:2])
            # print row_set[i][:2]
    return moments


# Rule based algorithm
"""
    extract after inbound and after timeout plays add to play_list
      for each play in play_list:
        initialize empty list as frame_list
        inside_count = 0
        for each frame in the play:
          [
          if all players are on one side of the court &
          ball is not held in the paint & inside_count <= 10:
            add the frame to frame_list
            inside_count = 0
          if ball is held in paint and inside_count <= 10
            add the frame to frame_list
            inside_count = inside_count + 1
          ] for length of frame_list >= 75 & frames added were contiguous:
                identify frame_list as action
"""


def segment_to_action(eid):
    return 0
