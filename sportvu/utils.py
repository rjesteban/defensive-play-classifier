import math


def get_moment(data, eid):
    diff = eid - int(data['events'][eid]['eventId'])
    if diff == 0:
        return data['events'][eid]['moments']
    else:
        currid = eid
        if diff > 0:
            while (diff > 0):
                diff = eid - int(data['events'][currid]['eventId'])
                currid += 1
            return data['events'][currid - 1]['moments']
        else:
            while(diff < 0):
                diff = eid - int(data['events'][currid]['eventId'])
                currid -= 1
            return data['events'][currid + 1]['moments']


def get_playerposition(data, pid):
    home = data['events'][0]['home']['players']
    visitor = data['events'][0]['visitor']['players']
    for player in home + visitor:
        if int(player['playerid']) == pid:
            return player['position']
    raise Exception("player not found")


def get_distance(p1, p2):
    sidex = math.fabs(p1[0] - p2[0])
    sidey = math.fabs(p1[1] - p2[1])
    return math.fabs(math.sqrt(sidex ** 2 + sidey ** 2))
