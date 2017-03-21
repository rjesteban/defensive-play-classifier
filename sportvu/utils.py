from playbyplay import utils as pbputil


def get_moment(data, eid):
    return data['events'][find_index(data, eid)]['moments']


def find_index(data, eid):
    for index, events in enumerate(data['events']):
        if events['eventId'] == str(eid):
            return index
    raise Exception("Index not found")


def get_playersoncourt(data, eid, side='home'):
    """
        returns players (ID, position, side, quarter) on court
        raises Exception if in that event there are more
        than or less than 11 PIDs
    """
    players = []
    index = find_index(data, eid)
    if side != 'home':
        side = 'visitor'
    p_dict = data['events'][index][side]['players']
    qtr = data['events'][index]['moments'][0][0]
    for frame in data['events'][index]['moments']:
        oncourt = [p[1] for p in frame[5]]
        if len(oncourt) != 11:
            raise Exception("Inconsistent number of players" +
                            " detected per frame")
        players += oncourt

    oncourt = set(players)
    if len(oncourt) != 11:
        raise Exception("Some sort of substitution happened in this event")
    # oncourt = [p[1] for p in data['events'][index]['moments'][0][5]]
    return ([[p['playerid'], str(p['position']), side, qtr]
            for p in p_dict if p['playerid'] in oncourt])


def contains(event, num, word):
    return event[num] is not None and word in str(event[num])


def determine_offs_defs(data, gameid, eid):
    pbp = pbputil.get_pbp(str(gameid))
    pbpindex = pbputil.find_index(pbp, eid)
    event = pbp['resultSets'][0]['rowSet'][pbpindex]
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
