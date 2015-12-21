# -*- coding: utf-8 -*-
__author__ = 'Semyon'

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import json


def weather_gen(is_demo):
    years = range(2003, 2016)
    months = range(1, 13)

    length = 12 * 12

    browser = webdriver.Firefox()

    script = "function getData(t){var e=$(\".dateText\"),r={};return e.each(function(t,e){var a=$(e),n=a.parent().parent(),i=a.text().trim(),p=n.find(\".show-for-large-up\").text().trim(),o=n.parent().parent().parent();console.log(1);var f=$(o.find(\".high .wx-value\")[0]).text().trim().replace(\"°\",\"\");r[\"\"+i]={weather:p,temperature:f}}),JSON.stringify(r)};"

    data = {}

    i = 0
    last_percent = -1

    for year in years:
        month_data = {}
        for month in months:
            i += 1
            percent = int((i / length) * 100)
            if percent > last_percent:
                last_percent = percent
                print(str(percent) + "%")
            url = 'http://www.wunderground.com/history/airport/KSFO/' + str(year) + '/' + str(month) + \
                  '/16/MonthlyCalendar.html?req_city=Сан-Франциско&req_state=&req_statename=California&reqdb.zip=&reqdb.magic=&reqdb.wmo='
            browser.get(url)
            # browser.implicitly_wait(3000)
            browser.execute_script(script)
            d = browser.execute_script(script + 'return getData(' + str(month) + ');')
            print(d)
            zz = json.loads(d)

            month_data[str(month)] = zz
        data[str(year)] = month_data
    ds = json.dumps(data)
    text_file = open("../data/new_weather.json" if not is_demo else "data/new_weather.json", "w")
    text_file.write(ds)
    text_file.close()


if __name__ == "__main__":
    weather_gen(False)
