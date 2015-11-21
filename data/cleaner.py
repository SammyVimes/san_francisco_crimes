# -*- coding: utf-8 -*-
import string
import pandas as pd
from data.input_reader import load
from dateutil.parser import parse

__author__ = 'Semyon'

day_of_week_map = {}

category_map = {}


def clean_train_set(filename, output_filename, log=False):
    last_day_of_week = -1
    last_category = -1

    initial_df = load(filename)
    length = initial_df.shape[0]
    arr = []
    last_percent = -1
    for i in range(len(initial_df.index)):
    # for i in range(1000):
        if log:
            percent = int((i / length) * 100)
            if percent > last_percent:
                last_percent = percent
                print(str(percent) + "%")
                print(str(i) + " строка")
        d = initial_df.index[i]
        row = initial_df.ix[i]

        day = d.day
        month = d.month
        year = d.year
        hour = d.hour
        minute = d.minute

        category = string.capwords(row['Category'])
        if category not in category_map:
            last_category += 1
            category_map[category] = last_category
        category = category_map[category]
        day_of_week = string.capwords(row['DayOfWeek'])
        if day_of_week not in day_of_week_map:
            last_day_of_week += 1
            day_of_week_map[day_of_week] = last_day_of_week
        day_of_week = day_of_week_map[day_of_week]
        lon = row['X']
        lat = row['Y']
        x = [day, month, year, hour, minute, day_of_week, lon, lat, category]
        arr.append(x)
    columns = ['day', 'month', 'year', 'hour', 'minute', 'day_of_week', 'lon', 'lat', 'category']
    new_df = pd.DataFrame(arr, columns=columns)
    new_df.to_csv(output_filename, index=False)


    clz = {}
    for v in category_map:
        clz[str(category_map[v])] = [v]
    clz_df = pd.DataFrame(clz)
    clz_df.to_csv(output_filename + '_classes', index=False)

    clz = {}
    for v in day_of_week_map:
        clz[str(day_of_week_map[v])] = [v]
    clz_df = pd.DataFrame(clz)
    clz_df.to_csv(output_filename + '_days', index=False)

    return day_of_week_map


def clean_test_set(filename, output_filename, day_of_week_map, log=False):
    initial_df = load(filename)
    length = initial_df.shape[0]
    arr = []
    last_percent = -1
    for i in range(length):
        if log:
            percent = int((i / length) * 100)
            if percent > last_percent:
                last_percent = percent
                print(str(percent) + "%")
                print(str(i) + " строка")
        row = initial_df.ix[i]

        d = parse(row["Dates"])

        day = d.day
        month = d.month
        year = d.year
        hour = d.hour
        minute = d.minute

        day_of_week = string.capwords(row['DayOfWeek'])
        day_of_week = day_of_week_map[day_of_week]
        lon = row['X']
        lat = row['Y']
        x = [day, month, year, hour, minute, day_of_week, lon, lat]
        arr.append(x)
    columns = ['day', 'month', 'year', 'hour', 'minute', 'day_of_week', 'lon', 'lat']
    new_df = pd.DataFrame(arr, columns=columns)
    new_df.to_csv(output_filename, index=False)
