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
    p_dict = data['events'][find_index(data, eid)][side]['players']
    oncourt = [p[1] for p in data['events'][index]['moments'][0][5]]
    return ([[p['playerid'], str(p['position'])]
            for p in p_dict if p['playerid'] in oncourt])
