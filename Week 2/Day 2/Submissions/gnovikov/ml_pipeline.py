import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def brand_target(brand):
    if 'Versace' in brand:
        val = 0
    elif 'Burberry' in brand:
        val = 1
    elif 'DnG' in brand:
        val = 2
    else:
        raise ValueError(f'Invalid brand: {brand}')
    return val


def apply_brand_loop(df):
    brand_list = []
    for i in range(len(df)):
        brand = df.iloc[i]['brand']
        target = brand_target(brand)
        brand_list.append(target)
    return brand_list


def process(dfs):
    df_brands = pd.concat([df.reset_index() for df in dfs])
    df_brands = df_brands.drop(columns=['index'])
    df_brands['words'] = df_brands['words'].str.upper()

    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(df_brands['words'])
    print(integer_encoded)

    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)

    brands_transformed = apply_brand_loop(df_brands.copy())
    y = brands_transformed

    X = onehot_encoded

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    models = {
        "Support vector (C=1.00)": SVC(C=1.00, gamma="scale"),
        "Support vector (C=0.25)": SVC(C=0.25, gamma="scale"),
        "Support vector (C=4.00)": SVC(C=4.00, gamma="scale"),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=1283220422),
        "Logistic Regression (C=1.00)": LogisticRegression(C=1.00, solver="liblinear", penalty="l1"),
        "Logistic Regression (C=0.25)": LogisticRegression(C=0.25, solver="liblinear", penalty="l1"),
        "Logistic Regression (C=4.00)": LogisticRegression(C=4.00, solver="liblinear", penalty="l1"),
        "1-nn euclidean": KNeighborsClassifier(n_neighbors=1),
        "1-nn cosine": KNeighborsClassifier(n_neighbors=1, metric="cosine"),
        "5-nn cosine": KNeighborsClassifier(n_neighbors=5, metric="cosine"),
    }

    for name, clf in models.items():
        clf.fit(X_train, y_train)

    scores = pd.Series({name: clf.score(X_test, y_test) for name, clf in models.items()}, name="Accuracy")
    print(scores)

