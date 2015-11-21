import os
import io
import codecs
import pandas as pd
import numpy as np
import string
import operator
from zipfile import ZipFile, is_zipfile
from contextlib import contextmanager

__author__ = 'Semyon'


def extract_csv(filepath):
    zp = ZipFile(filepath)
    csv = [f for f in zp.namelist() if os.path.splitext(f)[-1] == '.csv']
    return zp.open(csv.pop())


@contextmanager
def zip_csv_opener(filepath):
    fp = extract_csv(filepath) if is_zipfile(filepath) else open(filepath, 'rb')
    try:
        yield fp
    finally:
        fp.close()


def input_transformer(filepath):
    with zip_csv_opener(filepath) as fp:
        raw = fp.read().decode('utf-8')
    return pd.read_csv(io.StringIO(raw), parse_dates=True, index_col=0, na_values='NONE')


def load(name):
    cur_dir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(cur_dir, name)
    df = input_transformer(filename)
    return df
