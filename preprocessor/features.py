import numpy as np
from preprocessor.utils import determine_matchup
import math


distance = np.zeros((5, 5), dtype=np.int)


def get_entropy(action):
    entropy = []
    length = len(action.coords)
    for i in range(length):
        entropy.append(determine_matchup(action, i, "canonical"))

    entropy = sum(entropy)
    print "COUNT " * 10
    print entropy
    print "COUNT " * 10

    for r in range(len(entropy)):  # defenders
        for c in range(len(entropy[0])):  # offenders
            if entropy[r][c] > 0:
                p = entropy[r][c] / float(length)
                entropy[r][c] = -(p * math.log(p))
    # print("r: " + str(r) + ", c:" +
    # str(c) + " val:" +  str(p * math.log(p)))
    print "X" * 10 + "entropy" + "X" * 10
    print [sum(row) for row in entropy]
    print "X" * 10 + "entropy" + "X" * 10
    return entropy


def get_mean_distance(action):
    raise Exception("Distance: Not yet Implemented")


def get_number_passes(action):
    raise Exception("Passes: Not yet Implemented")
