import math


def get_distance(p1, p2):
    sidex = math.fabs(p1[0] - p2[0])
    sidey = math.fabs(p1[1] - p2[1])
    return math.fabs(math.sqrt(sidex ** 2 + sidey ** 2))


def transform_wlog(action):
    coordinates = []
    for entity in action.coords:
        for e in entity:
            x = e[2]
            y = e[3]
            if x > 47:
                e[2] = round(94 - x, 4)
            e[3] = round(50 - y, 4)
        coordinates.append(entity)
    action.coords = coordinates
    return action


def arrange_by_position(action):
    rank = {
        'C': 0,
        'C-F': 1,
        'F-C': 2,
        'F': 3,
        'F-G': 4,
        'G-F': 5,
        'G': 6
    }
    offense = range(len(action.offense))
    for i in range(len(action.offense)):
        j = i
        key = rank[action.offense[i][1]]
        while j > 0 and rank[str(offense[j - 1][1])] > key:
            offense[j] = offense[j - 1]
            j -= 1
        offense[j] = action.offense[i]

    defense = range(len(action.defense))
    for i in range(len(action.defense)):
        j = i
        key = rank[action.defense[i][1]]
        while j > 0 and rank[str(defense[j - 1][1])] > key:
            defense[j] = defense[j - 1]
            j -= 1
        defense[j] = action.defense[i]

    action.offense = offense
    action.defense = defense
    return action
