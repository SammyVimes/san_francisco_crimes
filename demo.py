__author__ = 'Semyon'

import data_preparation
from map import crime_map
from plot import crime_plot
import main
from weather import weather

crime_map.map_gen(True)
crime_plot.plot_gen(True)
weather.weather_gen(True)
data_preparation.data_gen()
main.train()
