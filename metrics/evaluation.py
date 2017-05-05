from sampling.bootstrap import bootstrap632
from sklearn.metrics import (confusion_matrix, roc_auc_score,
                             roc_curve, f1_score)
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

    # ([sensitivity, specificity, fscore, accuracy, auroc_score, matrix,
    #        [fpr, tpr, thresholds]])
    sensitivity_list = ([sens for (sens, spec, fscore, acc, auroc, matrix,
                        [fp, tp, th]) in metrics])
    specificity_list = ([spec for (sens, spec, fscore, acc, auroc, matrix,
                        [fp, tp, th]) in metrics])
    fscore_list = ([fscore for (sens, spec, fscore, acc, auroc, matrix,
                   [fp, tp, th]) in metrics])
    accuracy_list = ([acc for (sens, spec, fscore, acc, auroc, matrix,
                     [fp, tp, th]) in metrics])
    roc_auc_list = ([auroc for (sens, spec, fscore, acc, auroc, matrix,
                    [fp, tp, th]) in metrics])

    sensitivity_index = sensitivity_list.index(max(sensitivity_list))
    specificity_index = specificity_list.index(max(specificity_list))
    fscore_index = fscore_list.index(max(fscore_list))
    accuracy_index = accuracy_list.index(max(accuracy_list))
    roc_auc_index = roc_auc_list.index(max(roc_auc_list))

    best_acc = classifiers[accuracy_index]
    best_sens = classifiers[sensitivity_index]
    best_fscore = classifiers[fscore_index]
    best_spec = classifiers[specificity_index]
    best_auroc = classifiers[roc_auc_index]

    acc_metrics_train = metrics[accuracy_index]
    sens_metrics_train = metrics[sensitivity_index]
    fscore_metrics_train = metrics[fscore_index]
    spec_metrics_train = metrics[specificity_index]
    auroc_metrics_train = metrics[roc_auc_index]

    acc_metrics_test = get_metrics(best_acc, X_test, y_test)
    sens_metrics_test = get_metrics(best_sens, X_test, y_test)
    fscore_metrics_test = get_metrics(best_fscore, X_test, y_test)
    spec_metrics_test = get_metrics(best_spec, X_test, y_test)
    auroc_metrics_test = get_metrics(best_auroc, X_test, y_test)

    return {"acc_model": [best_acc, acc_metrics_train, acc_metrics_test],
            "sens_model": [best_sens, sens_metrics_train, sens_metrics_test],
            "spec_model": [best_spec, spec_metrics_train, spec_metrics_test],
            "auroc_model": ([best_auroc, auroc_metrics_train,
                            auroc_metrics_test]),
            "fscore_model": ([best_fscore, fscore_metrics_train,
                             fscore_metrics_test])
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

    accuracy = (sensitivity * (P / (P + N))) + (specificity * (N / (P + N)))

    yreshape = np.reshape(y, (len(y), 1))
    scores = clf.predict_proba(X)[:, 1]
    auroc_score = roc_auc_score(yreshape, scores, average='weighted')
    fpr, tpr, thresholds = roc_curve(y, scores, pos_label=1)
    fscore = f1_score(y, y_pred)
    return ([sensitivity, specificity, fscore, accuracy, auroc_score, matrix,
            [fpr, tpr, thresholds]])


def present_metrics(result, label):
    print "####### TRAIN " + label + " #######"
    print "SENSITIVITY: " + str(result[1][0])
    print "SPECIFICITY: " + str(result[1][1])
    print "FSCORE: " + str(result[1][2])
    print "ACCURACY: " + str(result[1][3])
    print "AUROC: " + str(result[1][4])
    print result[1][5]

    print "####### TEST " + label + " #######"
    print "SENSITIVITY: " + str(result[2][0])
    print "SPECIFICITY: " + str(result[2][1])
    print "FSCORE: " + str(result[2][2])
    print "ACCURACY: " + str(result[2][3])
    print "AUROC: " + str(result[2][4])
    print result[2][5]
