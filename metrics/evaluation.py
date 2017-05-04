from operator import itemgetter
from sampling.bootstrap import bootstrap632
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import confusion_matrix
import numpy as np


def evaluate_using_bootstrap(classifier, X, y, n_folds=10):
    acc_train = []
    acc_test = []
    clf_list = []
    for i in range(n_folds):
        X_train, X_test, y_train, y_test = bootstrap632(X, y)
        clf = classifier()
        clf.fit(X_train, y_train)
        clf_list.append(clf)

        y_pred = [clf.predict(x)[0] for x in X_test]
        y_train_pred = [clf.predict(x) for x in X_train]
        cf_train = confusion_matrix(y_train, y_train_pred, labels=[-1, 1])

        TN_train = cf_train[0][0] * 1.0
        FN_train = cf_train[1][0] * 1.0
        TP_train = cf_train[1][1] * 1.0
        FP_train = cf_train[0][1] * 1.0
        P_train = (TP_train + FN_train) * 1.0
        N_train = (TN_train + FP_train) * 1.0

        sensitivity_train = TP_train / P_train
        specificity_train = TN_train / N_train

        accuracy_train = ((sensitivity_train *
                          (P_train / (P_train + N_train))) +
                          (specificity_train *
                          (N_train / (P_train + N_train))))

        cf_test = confusion_matrix(y_test, y_pred, labels=[-1, 1])
        print cf_test
        TN_test = cf_test[0][0] * 1.0
        FN_test = cf_test[1][0] * 1.0
        TP_test = cf_test[1][1] * 1.0
        FP_test = cf_test[0][1] * 1.0
        P_test = (TP_test + FN_test) * 1.0
        N_test = (TN_test + FP_test) * 1.0

        sensitivity_test = TP_test / P_test
        specificity_test = TN_test / N_test

        accuracy_test = ((sensitivity_test * (P_test / (P_test + N_test))) +
                         (specificity_test * (N_test / (P_test + N_test))))
        acc_train.append(accuracy_train)
        acc_test.append(accuracy_test)

        print "sensitivity test: " + str(round(sensitivity_test, 5))
        print "specificity test: " + str(round(specificity_test, 5))
        print "   accuracy test: " + str(round(accuracy_test, 5))
        print ""

    acc_m = (0.632 * np.mean(acc_test)) + (0.368 * np.mean(acc_train))
    print "Accuracy of the model: " + str(acc_m)
    return acc_m, clf_list


def cross_validate_stratify(clf, X_train, X_test, y_train, y_test, fold=10):
    cv = []
    for i in range(fold):
        cv.append(train_test_split(X_train, y_train,
                  test_size=0.3, stratify=y_train))

    classifiers = []
    for (train_X, test_X, train_y, test_y) in cv:
        classifier = clf.fit(train_X, train_y)
        classifiers.append(classifier)

    metrics = ([get_metrics(svm, xtst, ytst)
               for svm, (xtr, xtst, ytr, ytst) in zip(classifiers, cv)])

    sensitivity_list = [sens for (sens, spec, acc, matrix) in metrics]
    specificity_list = [spec for (sens, spec, acc, matrix) in metrics]
    accuracy_list = [acc for (sens, spec, acc, matrix) in metrics]

    sensitivity_index = sensitivity_list.index(max(sensitivity_list))
    specificity_index = specificity_list.index(max(specificity_list))
    accuracy_index = accuracy_list.index(max(accuracy_list))

    best_acc = classifiers[accuracy_index]
    best_sens = classifiers[sensitivity_index]
    best_spec = classifiers[specificity_index]

    acc_metrics_train = metrics[accuracy_index]
    sens_metrics_train = metrics[sensitivity_index]
    spec_metrics_train = metrics[specificity_index]

    acc_metrics_test = get_metrics(best_acc, X_test, y_test)
    sens_metrics_test = get_metrics(best_sens, X_test, y_test)
    spec_metrics_test = get_metrics(best_spec, X_test, y_test)

    return {"acc_model": [best_acc, acc_metrics_train, acc_metrics_test],
            "sens_model": [best_sens, sens_metrics_train, sens_metrics_test],
            "spec_model": [best_spec, spec_metrics_train, spec_metrics_test]}


def get_metrics(clf, X, y):
    y_pred = [clf.predict(x) for x in X]
    matrix = confusion_matrix(y, y_pred, labels=[-1, 1])
    TN = matrix[0][0] * 1.0
    FN = matrix[1][0] * 1.0
    TP = matrix[1][1] * 1.0
    FP = matrix[0][1] * 1.0
    P = (TP + FN) * 1.0
    N = (TN + FP) * 1.0

    sensitivity = TP / P
    specificity = TN / N

    accuracy = (sensitivity * (P / (P + N))) + (specificity * (N / (P + N)))
    return sensitivity, specificity, accuracy, matrix


def present_metrics(acc, sens, spec):
    print "####### TRAIN ACC #######"
    print "ACCURACY: " + str(acc[1][2])
    print "SENSITIVITY: " + str(acc[1][0])
    print "SPECIFICITY: " + str(acc[1][1])
    print acc[1][3]

    print "####### TRAIN SENS #######"
    print "ACCURACY: " + str(sens[1][2])
    print "SENSITIVITY: " + str(sens[1][0])
    print "SPECIFICITY: " + str(sens[1][1])
    print sens[1][3]

    print "####### TRAIN SPEC #######"
    print "ACCURACY: " + str(spec[1][2])
    print "SENSITIVITY: " + str(spec[1][0])
    print "SPECIFICITY: " + str(spec[1][1])
    print spec[1][3]

    print ""

    print "####### TEST ACC #######"
    print "ACCURACY: " + str(acc[2][2])
    print "SENSITIVITY: " + str(acc[2][0])
    print "SPECIFICITY: " + str(acc[2][1])
    print acc[2][3]

    print "####### TEST SENS #######"
    print "ACCURACY: " + str(sens[2][2])
    print "SENSITIVITY: " + str(sens[2][0])
    print "SPECIFICITY: " + str(sens[2][1])
    print sens[2][3]

    print "####### TEST SPEC #######"
    print "ACCURACY: " + str(spec[2][2])
    print "SENSITIVITY: " + str(spec[2][0])
    print "SPECIFICITY: " + str(spec[2][1])
    print spec[2][3]
