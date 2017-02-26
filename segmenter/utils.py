# from action import Action
import json
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


def all_on_one_side(moment, eid):
    quarter = moment[0][0]
    #########################################################
    #                                                       #
    #             Check what quarter it is                  #
    #             Which side is attacking                   #
    #                                                       #
    #########################################################
    raise Exception("Not yet implemented.")