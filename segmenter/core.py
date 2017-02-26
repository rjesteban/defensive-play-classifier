from segmenter.utils import time_difference
from sportvu.utils import determine_offs_defs, get_playersoncourt, get_moment

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
            moments.append(row_set[i])
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
def convert_moment_to_action(data eid):
    moment = get_moment(data, eid)
    gameid = str(data['gameid'])
    players = determine_offs_defs(data, gameid, eid)
    
    #########################################################
    #                                                       #
    #                                                       #
    #             TODO: RULE BASED ALGORITHM                #
    #                                                       #
    #                                                       #
    #########################################################
    raise Exception(gameid, eventid, moment, players['offense'], players['defense']")