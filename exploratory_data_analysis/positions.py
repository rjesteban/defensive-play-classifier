import json

PATH = 'data/sportvu/'
ids = ['0021500316', '0021500270', '0021500149', '0021500198',
       '0021500428', '0021500350', '0021500336', '0021500476', '0021500582']


positions = []
for id in ids:
    data = json.load(open(PATH + id + '.json'))
    players = (data['events'][0]['home']['players'] +
               data['events'][0]['visitor']['players'])
    pos = [str(p['position']) for p in players]
    for p in pos:
        positions.append(p)

print sorted(set(positions))

# ['C', 'C-F', 'F', 'F-C', 'F-G', 'G', 'G-F']
