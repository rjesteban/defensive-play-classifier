from action.core import load_action
from preprocessor.features import *
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
import json
import numpy as np

PATH = "data/actions/"

"""
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
"""
# X = np.matrix([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4],
#               [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]])
# y = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
X = []
y = []
gameids = ["0021500149", "0021500197", "0021500270", "0021500316",
           "0021500350", "0021500428", "0021500476", "0021500582"]
print "LOADING ACTIONS..."
for gid in gameids:
    data = json.load(open(PATH + gid + ".json"))
    for eid in sorted(data.keys()):
        action = load_action(gid, eid)
        X.append([get_DTW(action), get_mean_distance(action),
                  get_entropy(action)])
        y.append(int(action.label))
print "SPLITTING DATA..."
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.3,
                                                    stratify=y)

print str('*' * 10) + "TRAINING"
print X_train
print ''
print y_train
print ''

print str('*' * 10) + "TESTING"
print X_test
print ''
print y_test
print ''

print "BUILDING MODEL..."
clf = SVC()
clf.fit(X_train, y_train)
y_pred = [clf.predict(x) for x in X_test]

print "SHOWING METRICS..."
print confusion_matrix(y_test, y_pred, labels=[0, 1])
print clf.score(X_test, y_test)
