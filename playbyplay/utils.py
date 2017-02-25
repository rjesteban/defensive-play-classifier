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
    if not os.path.exists(os.path.dirname('../data/pbp/')):
        os.makedirs('pbp')
    with open('../data/pbp/' + id + 'pbp.json', 'w') as file:
        json.dump(data, file)
