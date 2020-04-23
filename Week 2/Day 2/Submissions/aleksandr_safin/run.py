import argparse
from data import get_data
from clfs import create_models
from sklearn.model_selection import train_test_split


def set_args(parser):
    parser.add_argument('--test_size', type=float,
                        default=0.33, help='test size for data train/test split')
    parser.add_argument('--random_state', type=int,
                        default=42, help='random state seed')
    return parser


def main(args):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=args.random_state)
    X, y = get_data()
    
    models = create_models(None)
    models = dict(models)
    
    for name, clf in models.items():
        clf.fit(X_train, y_train)
    scores = pd.Series({name: clf.score(X_test, y_test) for name, clf in models.items()}, name="Accuracy")
    print(scores)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    set_args(parser)
    args = parser.parse_args()
    
    main()
