from preprocessor.features import (get_entropy, get_mean_distance,
                                   get_mean_distance_from_canonical_position)
from action.core import load_action
import json


PATH = "data/actions/"
gids = ["0021500149", "0021500197", "0021500270", "0021500316",
        "0021500350", "0021500428", "0021500476", "0021500582"]



yy = []

for gid in gids:
    data = json.load(open(PATH + gid + ".json"))
    for eid in sorted(data.keys()):
        action = load_action(gid, eid)
        entropy = get_entropy(action)
        # mean_distance = get_mean_distance(action)
        dist = get_mean_distance_from_canonical_position(action)
        row = [str(gid), str(eid)] + [str(e) for e in entropy] + [str(d) for d in dist] + [str(action.label)]
        yy.append(row)
        print ', '.join(row)
