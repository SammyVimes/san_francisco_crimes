# -*- coding: utf-8 -*-
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import xgboost as xgb

__author__ = 'Semyon'


def train():
    from data import input_reader
    import pandas as pd

    print("Читаем трейнсет")
    train_csv = input_reader.load("data/clean_train.csv")
    train_true = train_csv['category'].tolist()
    train_csv = train_csv.drop('category', 1)
    train_features = train_csv.as_matrix()

    sz = 600000

    train__train_features = train_features[:sz, :]
    train__train_true = train_true[:sz]

    train__test_features = train_features[sz:, :]
    train__test_true = train_true[sz:]

    model = xgb.XGBClassifier(max_depth=80, n_estimators=30, learning_rate=0.05, nthread=4, subsample=0.7,
                              colsample_bytree=0.7, silent=True)
    print("Учимся")
    model.fit(train__train_features, train__train_true)

    print("Оцениваем на части трейна")
    score = model.score(train__test_features, train__test_true)
    print("Результат =", score)

    print("Учимся на полном сете")
    model.fit(train_features, train_true)

    print("Читаем тест сет")
    test_csv = input_reader.load("data/clean_test.csv")
    test_features = test_csv.as_matrix()
    print("Предсказываем вероятности")
    predicted_probas = model.predict_proba(test_features)



    # выводим классы
    cur_dir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(cur_dir, "data/clean_train.csv_classes")
    clz_map = pd.read_csv(filename, index_col=False)
    r = clz_map.ix[0]

    cols = [r[str(c)].upper() for c in model.classes_]

    print(cols)

    print("Пишем результат")
    res_df = pd.DataFrame(predicted_probas, columns=cols)
    res_df.to_csv("data/res.csv", index=True, index_label="Id")
    print("Готово!")


if __name__ == "__main__":
    train()