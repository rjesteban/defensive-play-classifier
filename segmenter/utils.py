import math

PBP_PATH = 'data/pbp/'


def time_difference(time1, time2):
    time_1 = [int(i) for i in time1.split(':')]
    time_2 = [int(i) for i in time2.split(':')]
    t1 = (time_1[0] * 60) + time_1[1]
    t2 = (time_2[0] * 60) + time_2[1]
    if t1 < t2:
        raise Exception(time1 + " is less than " + time2)
    return int(math.fabs(t1 - t2))


def all_on_one_side(m, eid, frame):
    return len(set([0 if coord[2] < 47 else 1 for coord in m[frame][5]])) == 1


def within_the_paint(entity, eid):
    x, y = entity[2], entity[3]
    return (0 <= x <= 19 or (94 - 19) <= x <= 94 and
            (25 - 12) <= y <= (25 + 12))
