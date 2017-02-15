import json
import os
import requests


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

    for i in range(len(row_set)):
        if ((1 <= row_set[i][2] <= 2 or row_set[i][2] == 5) and
           row_set[i - 1][2] != 5):
            moments.append(row_set[i][:3])
    return moments


if __name__ == '__main__':
    ids = ['0021500316', '0021500270', '0021500149', '0021500197',
           '0021500428', '0021500350', '0021500336',
           '0021500476', '0021500582']

    for id in ids:
        acquire_pbp_json(id)
