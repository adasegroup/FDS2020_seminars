from sklearn.dummy import DummyClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier


class ModelDisc():
    def __init__(self, name, model):
        self.name = name
        self.model = model

def create_models(models_disc):
    models = []
    models.append(("Baseline", DummyClassifier(random_state=391488407)))
    models.append(("Support vector (C=1.00)", SVC(C=1.00, gamma="scale")))
    models.append(("Support vector (C=0.25)", SVC(C=0.25, gamma="scale")))
    models.append(("Support vector (C=4.00)", SVC(C=4.00, gamma="scale")))

    models.append(("Random Forest", RandomForestClassifier(n_estimators=100, random_state=1283220422)))


    models.append(("Logistic Regression (C=1.00)",
                   LogisticRegression(C=1.00, solver="liblinear", penalty="l1")))

    models.append(("Logistic Regression (C=0.25)",
                   LogisticRegression(C=0.25, solver="liblinear", penalty="l1")))

    models.append(("Logistic Regression (C=4.00)",
                   LogisticRegression(C=4.00, solver="liblinear", penalty="l1")))
    models.append(("1-nn euclidean",
                   KNeighborsClassifier(n_neighbors=1)))

    models.append(("1-nn cosine",
                   KNeighborsClassifier(n_neighbors=1, metric="cosine")))

    models.append(("5-nn cosine",
                   KNeighborsClassifier(n_neighbors=5, metric="cosine")))
#     for md in models_disc:
#         models.append((md.name, md.model))
    return models



