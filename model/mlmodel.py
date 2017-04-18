from sklearn.svm import SVC

def create_SVC_balanced():
    return SVC(class_weight='balanced')

def create_SVC():
    return SVC()
