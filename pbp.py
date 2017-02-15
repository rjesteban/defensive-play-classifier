import json
import math
import os
import requests


def time_difference(time1, time2):
    time_1 = [int(i) for i in time1.split(':')]
    time_2 = [int(i) for i in time2.split(':')]
    t1 = (time_1[0] * 60) + time_1[1]
    t2 = (time_2[0] * 60) + time_2[1]
    return int(math.fabs(t1 - t2))


def acquire_pbp_json(id):
    header_data = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
        ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 '
        'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'
        ',image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }

    game_url = ('http://stats.nba.com/stats/playbyplayv2?' +
                'EndPeriod=0&EndRange=0&GameID=' + id +
                '&RangeType=0&StartPeriod=0&StartRange=0')
    response = requests.get(game_url, headers=header_data)
    data = response.json()
    if not os.path.exists(os.path.dirname('pbp/')):
        os.makedirs('pbp')
    with open('pbp/' + id + 'pbp.json', 'w') as file:
        json.dump(data, file)


def pick_possessions(pbp):
    """
    picks ids of moments ending in a shot, or a steal.
    do not pick moments where the previous moment was a steal.
    pick after timeout/violation/substitution/foul moments.

    Keyword argument:
    pbp -- file name (str)
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
                           row_set[i - 1][6]) < 5)
        follow_up = (row_set[i - 1][2] == 4 and
                     time_difference(row_set[i - 1][6], row_set[i - 1][6]) < 5)
        attempt = (shot_attempt and not follow_up) or turnover or stop_play
        if attempt and not came_from_steal:
            moments.append(row_set[i][:3])
    return moments


if __name__ == '__main__':
    ids = ['0021500316', '0021500270', '0021500149', '0021500197',
           '0021500428', '0021500350', '0021500336',
           '0021500476', '0021500582']
    # ids = ['0021500582']
    moments = []

    for id in ids:
        # acquire_pbp_json(id)
        moments += pick_possessions('pbp/' + id + 'pbp.json')
    print len(moments)
