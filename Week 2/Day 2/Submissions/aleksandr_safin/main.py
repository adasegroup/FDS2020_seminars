from data import get_data
from clfs import create_models
import pandas as pd
from sklearn.model_selection import train_test_split

def main(args):
    X, y = get_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=args.random_state)

    models = create_models(None)
    models = dict(models)
    
    for name, clf in models.items():
        clf.fit(X_train, y_train)
    scores = pd.Series({name: clf.score(X_test, y_test) for name, clf in models.items()}, name="Accuracy")
    print(scores)