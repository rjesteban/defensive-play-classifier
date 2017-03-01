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
