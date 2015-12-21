# -*- coding: utf-8 -*-
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import xgboost as xgb

__author__ = 'Semyon'

from data import cleaner


def data_gen():
    dowm, wtm = cleaner.clean_train_set("data/train.csv.zip", "data/clean_train.csv", "data/new_weather.json", log=True)
    cleaner.clean_test_set("data/test.csv.zip", "data/clean_test.csv", dowm, wtm, "data/new_weather.json", log=True)


if __name__ == "__main__":
    data_gen()
