from sampling.bootstrap import bootstrap632
from sklearn.metrics import (confusion_matrix, matthews_corrcoef)
import math
import numpy as np


def evaluate_using_bootstrap(classifier, X, y, n_folds=10):
    gmean_train = []
    gmean_test = []
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

        gmean_train = math.fabs(math.sqrt(sensitivity_train *
                                specificity_train))

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

        gmean_test = math.fabs(math.sqrt(sensitivity_test * specificity_test))
        gmean_train.append(gmean_train)
        gmean_test.append(gmean_test)

        print "sensitivity test: " + str(round(sensitivity_test, 5))
        print "specificity test: " + str(round(specificity_test, 5))
        print "      gmean test: " + str(round(gmean_test, 5))
        print ""

    gmean_m = (0.632 * np.mean(gmean_test)) + (0.368 * np.mean(gmean_train))
    print "gmean of the model: " + str(gmean_m)
    return gmean_m, clf_list


def cross_validate_stratify(clf, X_train, X_test, y_train, y_test, skf):
    cv = []
    classifiers = []
    for train_index, test_index in skf:
        train_X, test_X = X_train[train_index], X_train[test_index]
        train_y, test_y = y_train[train_index], y_train[test_index]
        classifiers.append(clf.fit(train_X, train_y))
        cv.append([train_X, test_X, train_y, test_y])

    metrics = ([get_metrics(svm, xtst, ytst)
               for svm, (xtr, xtst, ytr, ytst) in zip(classifiers, cv)])

    # sensitivity, specificity, matthews, gmean, matrix
    sensitivity_list = [sens for (sens, spec, matt, gmean, matrix) in metrics]
    specificity_list = [spec for (sens, spec, matt, gmean, matrix) in metrics]
    matthews_list = [matt for (sens, spec, matt, gmean, matrix) in metrics]
    gmean_list = [gmean for (sens, spec, matt, gmean, matrix) in metrics]

    sensitivity_index = sensitivity_list.index(max(sensitivity_list))
    specificity_index = specificity_list.index(max(specificity_list))
    matthews_index = matthews_list.index(max(matthews_list))
    gmean_index = gmean_list.index(max(gmean_list))

    best_sens = classifiers[sensitivity_index]
    best_spec = classifiers[specificity_index]
    best_matt = classifiers[matthews_index]
    best_gmean = classifiers[gmean_index]

    sens_metrics_train = metrics[sensitivity_index]
    spec_metrics_train = metrics[specificity_index]
    matt_metrics_train = metrics[matthews_index]
    gmean_metrics_train = metrics[gmean_index]

    sens_metrics_test = get_metrics(best_sens, X_test, y_test)
    spec_metrics_test = get_metrics(best_spec, X_test, y_test)
    matt_metrics_test = get_metrics(best_matt, X_test, y_test)
    gmean_metrics_test = get_metrics(best_gmean, X_test, y_test)

    return {"sens_model": [best_sens, sens_metrics_train, sens_metrics_test],
            "spec_model": [best_spec, spec_metrics_train, spec_metrics_test],
            "matt_model": [best_matt, matt_metrics_train, matt_metrics_test],
            "gmean_model": ([best_gmean, gmean_metrics_train,
                            gmean_metrics_test]),
            }


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

    gmean = math.fabs(math.sqrt(sensitivity * specificity))
    matthews = matthews_corrcoef(y, y_pred)

    return sensitivity, specificity, matthews, gmean, matrix


def present_metrics(result, label):
    print "####### TRAIN " + label + " #######"
    print "SENSITIVITY: " + str(result[1][0])
    print "SPECIFICITY: " + str(result[1][1])
    print "MATTHEWS CORR COEF: " + str(result[1][2])
    print "GMEAN: " + str(result[1][3])
    print result[1][4]
    print ""
    print "####### TEST " + label + " #######"
    print "SENSITIVITY: " + str(result[2][0])
    print "SPECIFICITY: " + str(result[2][1])
    print "MATTHEWS CORR COEF: " + str(result[2][2])
    print "GMEAN: " + str(result[2][3])
    print result[2][4]
