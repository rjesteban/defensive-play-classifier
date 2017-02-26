from playbyplay import utils as pbputil


def get_moment(data, eid):
    return data['events'][find_index(data, eid)]['moments']


def find_index(data, eid):
    index = eid
    diff = eid - int(data['events'][eid]['eventId'])
    if diff == 0:
        return index
    if diff > 0:
        while (diff > 0):
            diff = eid - int(data['events'][index]['eventId'])
            index += 1
        return index - 1
    else:
        while(diff < 0):
            diff = eid - int(data['events'][index]['eventId'])
            index -= 1
        return index + 1


def get_playersoncourt(data, eid, side='home'):
    index = find_index(data, eid)
    if side != 'home':
        side = 'visitor'
    p_dict = data['events'][index][side]['players']
    qtr = data['events'][index]['moments'][0][0]
    oncourt = [p[1] for p in data['events'][index]['moments'][0][5]]
    return ([[p['playerid'], str(p['position']), side, qtr]
            for p in p_dict if p['playerid'] in oncourt])


def contains(event, num, word):
    return event[num] is not None and word in str(event[num])


def determine_offs_defs(data, gameid, eid):
    pbp = pbputil.get_pbp(str(gameid))
    event = pbp['resultSets'][0]['rowSet'][pbputil.find_index(pbp, eid)]
    if (event[2] in [1, 2] and event[7] is not None and
       ('Shot' or 'MISS' in str(event[7])) or
       event[2] == 5 and contains(event, 7, 'Turnover') or
       event[2] == 6 and contains(event, 9, 'S.FOUL')):
        # away ang defense
        offense = get_playersoncourt(data, eid)
        defense = get_playersoncourt(data, eid, side='visitor')
        return {'offense': offense, 'defense': defense}
    elif (event[2] in [1, 2] and event[9] is not None and
          'Shot' or 'MISS' in str(event[9]) or
          event[2] == 5 and contains(event, 9, 'Turnover') or
          event[2] == 6 and contains(event, 7, 'S.FOUL')):
        # home ang defense
        offense = get_playersoncourt(data, eid, side='visitor')
        defense = get_playersoncourt(data, eid)
        return {'offense': offense, 'defense': defense}
    raise Exception("Not an event")
