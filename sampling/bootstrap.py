import numpy as np
import random


def bootstrap632(X, y):
    d = len(y)
    training_indices = []
    for index in range(d):
        training_indices.append(random.randint(0, d - 1))
    testing_indices = [i for i in range(d) if i not in training_indices]
    train_X = np.concatenate([X[i] for i in training_indices])
    train_y = np.array([y[i] for i in training_indices])
    test_X = np.concatenate([X[i] for i in testing_indices])
    test_y = np.array([y[i] for i in testing_indices])
    return train_X, test_X, train_y, test_y
