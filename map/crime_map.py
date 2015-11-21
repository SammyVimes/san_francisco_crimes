# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np
import string
import matplotlib.cm as cm
import matplotlib as mpl
from data.input_reader import load
import math
from PIL import Image
from PIL import ImageDraw

__author__ = 'Semyon'


def rad2deg(d):
    return (d * 180) / math.pi


def deg2rad(d):
    return (d * math.pi) / 180


earth_radius = 6378137


def lat2y_m(lat):
    return earth_radius * math.log(math.tan(math.pi / 4 + deg2rad(lat) / 2))


def lon2x(lon):
    return deg2rad(lon) * earth_radius


width = 1038  # хардкод ширины
height = 1095  # хардкод высоты

# левая верхняя точка
lon_l = -122.51456
lat_l = 37.81155

# правая нижняя точка
lon_r = -122.37173
lat_r = 37.69238

lx = lon2x(lon_l)
ly = lat2y_m(lat_l)
rx = lon2x(lon_r)
ry = lat2y_m(lat_r)
real_width = math.fabs(rx - lx)
real_height = math.fabs(ry - ly)


# широта долгота в точки на картинке
def calc_on_map_point(lon, lat):
    px = lon2x(lon)
    py = lat2y_m(lat)

    # реальные точки, но относительно левого края картинки
    local_x = math.fabs(px - lx)
    local_y = math.fabs(py - ly)

    # точки на картинке (делим относительную точку на реальный размер и умножаем на размер картинки)
    img_x = (local_x / real_width) * width
    img_y = (local_y / real_height) * height
    return (img_x, img_y)


rad = 5


def point_to_ellipse(p):
    return p[0] - rad, p[1] - rad, p[0] + rad, p[1] + rad


x = []  # longitudes
y = []  # latitudes

df = load("../data/train.csv.zip")

cur_dir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(cur_dir, '../data/map.png')
image = Image.open(filename)
draw = ImageDraw.Draw(image)

for i in range(100):
    first_row = df.ix[i]
    lon = first_row["X"]
    lat = first_row["Y"]
    p = calc_on_map_point(lon, lat)
    draw.ellipse(point_to_ellipse(p), fill='blue', outline='blue')


#draw.point(p, 'red')
image.save('test.png')
