#!/usr/bin/python3

import influxdb
import json
from database.time_series import config
import time
import datetime
import random


conn = influxdb.InfluxDBClient(
    host      = "localhost",
    port      = 32790,
    username  = config.USERNAME,
    password  = config.PASSWORD,
    database  = config.DATABASE,
    pool_size = config.POOL_SIZE
)

timestamp = int(time.mktime(datetime.datetime(2019,5,15).timetuple()))
last_timestamp = time.mktime(datetime.datetime(2019, 5, 16).timetuple())

latitude = 40.107565
longitude = -101.430733

to_write = []

while timestamp < last_timestamp:
    if random.random() < 0.1:
        point = {
          "measurement": "Event",
          "time": timestamp,
          "tags": {
              "username": "aspedrosa2"
          },
          "fields": {
              "events": "{\"events\":[\"Dor de cabeça\",\"Dor de cenas\"],\"metrics\": [\"PersonalStatus\",\"PersonalStatus\"],\"data\":{}}",
              "latitude": latitude,
              "longitude": longitude
          }
        }
        to_write.append(point)
        

    point = {
      "measurement": "Path",
      "time": timestamp,
      "tags": {
          "username": "aspedrosa2"
      },
      "fields": {
          "latitude": latitude,
          "longitude": longitude
      }
    }

    to_write.append(point)

    timestamp += 10 * 60

    rand = random.random()
    if rand < 0.33:
        if rand < 0.15:
            latitude += 0.1
        else:
            latitude -= 0.1
    elif rand < 0.66:
        if rand < 0.45:
            longitude += 0.1
        else:
            longitude -= 0.1
    else:
        rand = random.random()
        if rand < 0.25:
            latitude += 0.1
            longitude += 0.1
        elif rand < 0.5:
            latitude += 0.1
            longitude -= 0.1
        elif rand < 0.75:
            latitude -= 0.1
            longitude += 0.1
        else:
            latitude -= 0.1
            longitude -= 0.1


conn.write_points(to_write, 's')
