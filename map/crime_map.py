# -*- coding: utf-8 -*-
import operator
import os
import string
import math

from PIL.ImageFont import truetype
from PIL import Image
from PIL import ImageDraw

from data.input_reader import load
from translator.yandex import translate

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


cur_dir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(cur_dir, '../data/map.png')
image = Image.open(filename)

width, height = image.size

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


rad = 2


def point_to_ellipse(p):
    return p[0] - rad, p[1] - rad, p[0] + rad, p[1] + rad


x = []  # longitudes
y = []  # latitudes


print("Загружаем датасет")
df = load("../data/train.csv.zip")
print("Загружено")

i = Image.new("RGBA", (width, height), 'white')
d = ImageDraw.Draw(i, "RGBA")

i.paste(image)
# draw = ImageDraw.Draw(image, "RGBA")
draw = d
image = i


def top_crimes(df, items=0):
    df.columns = df.columns.map(operator.methodcaller('lower'))
    by_col = df.groupby("category")
    col_freq = by_col.size()
    col_freq.index = col_freq.index.map(string.capwords)
    col_freq.sort(ascending=False, inplace=True)
    cols = [col for col in col_freq.index]
    cols = cols[0:1] + cols[3:]
    return cols[:items]


print("Достаём топ-5 преступлений")
top = top_crimes(df, items=5)

opacity = 220
# color_list = ['red', 'green', 'blue', 'purple', 'orange', 'pink', 'black', 'brown']
color_list = [(255, 0, 0, opacity), (0, 255, 0, opacity), (0, 0, 255, opacity), (255, 127, 80, opacity),
              (139, 0, 139, opacity), (255, 105, 180, opacity), (0, 0, 0, opacity),
              (188, 143, 143, opacity)]

colors_map = {top[i]: color_list[i] for i in range(len(top))}

print("Начинаем рисовать на карте")
length = df.shape[0]
last_percent = -1
for i in range(length):
    percent = int((i / length) * 100)
    if percent > last_percent:
        last_percent = percent
        print(str(percent) + "%")
        print(str(i) + " строка")
    first_row = df.ix[i]
    category = string.capwords(first_row["category"])
    if category in top:
        lon = first_row["x"]
        lat = first_row["y"]
        p = calc_on_map_point(lon, lat)
        color = colors_map[category]
        draw.ellipse(point_to_ellipse(p), fill=color, outline=color)


# рисуем легенду


lineheight = 35
padding = 20
space = 20
legend_rad = 10
font = truetype(font="times.ttf", size=15)
legend_right = width / 3
legend_down = (len(top)) * lineheight + padding
draw.rectangle((0, 0, legend_right, legend_down), 'white', 'black')
for i in range(len(top)):
    x = padding
    y = i * lineheight + padding
    category = top[i]
    color = colors_map[category]
    draw.ellipse((x, y, x + (2 * legend_rad), y + (2 * legend_rad)), fill=color, outline='black')
    draw.text((x + (2 * legend_rad) + space, y), translate(category, "en", "ru"), fill='black', font=font)

image.save('test.png', 'PNG')
