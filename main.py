import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import xgboost as xgb

__author__ = 'Semyon'

from data import cleaner

# dowm = cleaner.clean_train_set("data/train.csv.zip", "data/clean_train.csv", log=True)
# cleaner.clean_test_set("data/test.csv.zip", "data/clean_test.csv", dowm, log=True)

from data import input_reader
import pandas as pd


print("������ ��������")
train_csv = input_reader.load("data/clean_train.csv")
train_features = train_csv.as_matrix()
train_true = train_csv['category'].tolist()

train__train_features = train_features[:600000, :]
train__train_true = train_true[:600000]

train__test_features = train_features[600000:, :]
train__test_true = train_true[600000:]

model = xgb.XGBClassifier(max_depth=100, n_estimators=100, learning_rate=0.05, nthread=4, silent=True)
print("������")
model.fit(train__train_features, train__train_true)

print("��������� �� ����� ������")
score = model.score(train__test_features, train__test_true)
print("��������� =", score)

print("������ �� ������ ����")
model.fit(train_features, train_true)


print("������ ���� ���")
test_csv = input_reader.load("data/clean_test.csv")
test_features = test_csv.as_matrix()
print("������������� �����������")
predicted_probas = model.predict_proba(test_features)



#������� ������
cur_dir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(cur_dir, "data/clean_train.csv_classes")
clz_map = pd.read_csv(filename, index_col=False)
r = clz_map.ix[0]

cols = [r[str(c)].upper() for c in model.classes_]

print(cols)

print("����� ���������!")
res_df = pd.DataFrame(predicted_probas, columns=cols)
res_df.to_csv("data/res.csv", index=True, index_label="Id")
