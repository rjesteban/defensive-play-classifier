def acquire_gameData(id):
    import requests
    import json
    header_data = {  #  I pulled this header from the py goldsberry library
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'\
        ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 '\
        'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'\
        ',image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }

    game_url = 'http://stats.nba.com/stats/playbyplayv2?EndPeriod=0&EndRange=0&GameID='+ id +\
                '&RangeType=0&StartPeriod=0&StartRange=0'   #  address for querying the data
    response = requests.get(game_url,headers = header_data)  #  go get the data
    data = response.json()
    with open('pbp/' + id + 'pbp.json', 'w') as file:
        json.dump(data, file)


if __name__ == '__main__':
    ids = ['0021500316', '0021500270', '0021500149', '0021500197', 
           '0021500428', '0021500350', '0021500336', '0021500476', '0021500582']

    for id in ids:
        acquire_gameData(id)
  