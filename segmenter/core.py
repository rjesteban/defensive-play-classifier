from action.core import Action
from segmenter.utils import (time_difference, all_on_one_side,
                             within_the_paint, less_than, format_time)
from preprocessor.utils import transform_wlog
from playbyplay.utils import get_play
from sportvu.utils import get_moment, determine_offs_defs
import json

PBP_PATH = 'data/pbp/'


# time difference quota is still under experiment, EDA needed
def pick_possessions(gameid):
    """
    picks ids of moments ending in a shot, or a steal.
    do not pick moments where the previous moment was a steal.
    pick after timeout/violation/substitution/foul moments.

    Keyword argument:
    gameid -- file name (str)

    returns:
        array of gameid, eventid
    """
    data = json.load(open(PBP_PATH + gameid + 'pbp.json'))
    row_set = data['resultSets'][0]['rowSet']
    moments = []

    for i in range(1, len(row_set)):
        if ((row_set[i][7] is not None and 'S.FOUL' in row_set[i][7]) or
           (row_set[i][9] is not None and 'S.FOUL' in row_set[i][9])):
            shot_foul = True
        else:
            shot_foul = False
        shot_attempt = ((1 <= row_set[i][2] <= 2) or shot_foul)
        turnover = row_set[i][2] == 5
        # stop_play = row_set[i][2] in [7, 9] and
        # row_set[i - 1][2] not in [7, 9]
        if ((row_set[i][7] is not None and 'Timeout' in row_set[i][7]) or
           (row_set[i][9] is not None and 'Timeout' in row_set[i][9]) or
           (row_set[i][7] is None and row_set[i][9] is None)):
            timeout = True
        else:
            timeout = False
        came_from_steal = (row_set[i - 1][2] == 5 and
                           row_set[i - 1][3] <= 2 and
                           time_difference(row_set[i - 1][6],
                           row_set[i][6]) < 5)
        follow_up = (row_set[i - 1][2] == 4 and
                     time_difference(row_set[i - 1][6], row_set[i][6]) < 5)
        attempt = (shot_attempt and not follow_up) or turnover  # or stop_play
        if attempt and not came_from_steal and not timeout:
            moments.append(row_set[i][1])
    return moments


# Rule based algorithm
def convert_moment_to_action(data, eid, check_frames=True, label=0):
    play = get_play(str(data['gameid']), eid)
    end_time = play[6]
    end_min = int(end_time.split(':')[0])
    end_sec = int(end_time.split(':')[1])
    moment = get_moment(data, eid)
    gameid = str(data['gameid'])
    frames = []
    prev_frames = []
    inside_count = 0
    for fr, frame in enumerate(moment):
        ball = moment[fr][5][0]
        mins = int(moment[fr][2] / 60)
        secs = int(((moment[fr][2] / 60.0) - mins) * 60)
        if less_than(mins, secs, end_min, end_sec):
            break
        if all_on_one_side(moment, eid, fr):
            frames.append(frame)
            if within_the_paint(ball, eid):
                inside_count += 1
            else:
                inside_count = 0
            # height of ball: ball[4]
            # if inside_count > 50 or ball[4] > 12 and len(frames) >= 120:
            if ball[4] > 13 and len(frames) >= 130:
                prev_frames = frames
                frames = []
                inside_count = 0
        else:
            if len(frames) >= 130:
                prev_frames = frames
            inside_count = 0
            frames = []
    if check_frames and (len(frames) < 130):
        if len(prev_frames) >= 130:
            frames = prev_frames
        else:
            raise Exception("Insufficient number of frames: " +
                            str(len(frames)) + " | " + str(len(prev_frames)))
    players = determine_offs_defs(data, gameid, eid)
    offense = players['offense']
    defense = players['defense']
    coords = [coord[5] for coord in frames]
    quarter = frames[0][0]
    the_time = [format_time(time[2]) for time in frames]
    action = Action(gameid=gameid, eid=eid, coords=coords,
                    time=the_time, quarter=quarter,
                    offense=offense, defense=defense, label=label)
    transform_wlog(action)
    return action
