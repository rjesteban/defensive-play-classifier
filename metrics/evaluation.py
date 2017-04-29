from sampling.bootstrap import bootstrap632
from sklearn.metrics import confusion_matrix
import numpy as np


def evaluate_using_bootstrap(classifier, X, y, k=10):
    k = 10
    acc_train = []
    acc_test = []
    for i in range(k):
        X_train, X_test, y_train, y_test = bootstrap632(X, y)
        clf = classifier()
        clf.fit(X_train, y_train)

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
    return acc_m
