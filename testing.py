from action.core import load_action
from preprocessor.features import *

print str("*" * 20) + "zone" + str("*" * 20)
for eid in [364, 375, 381, 392, 404]:
    action = load_action("0021500149", eid)
    print "EID: " + str(eid)
    print "DTW: " + str(np.mean(get_DTW(action)))
    print "AVG: " + str(np.mean(get_mean_distance(action)))
    print "ENT: " + str(np.mean(get_entropy(action)))
    print ''
print str("*" * 20) + "man" + str("*" * 20)
for eid in [33, 90, 97, 328, 555]:
    action = load_action("0021500149", eid)
    print "EID: " + str(eid)
    print "DTW: " + str(np.mean(get_DTW(action)))
    print "AVG: " + str(np.mean(get_mean_distance(action)))
    print "ENT: " + str(np.mean(get_entropy(action)))
    print ''
