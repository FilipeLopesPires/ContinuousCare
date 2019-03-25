#!/usr/bin/python3

__all__ = [
        "Database"
        ]

import time

import influxdb


class Database:
    def __init__(self):
        self.client = influxdb.InfluxDBClient()
        self.client.create_database("db")
        self.client.switch_database("db")

    def insert(self, data, lat, longi, clientId, deviceId):
        points = []

        for metric, val in data.items():
            point = {
                "measurement": metric,
                "tags": {
                    "clientId": clientId,
                    "deviceId": deviceId,
                },
                "time": int(time.time()),
                "fields": {
                    "value": val,
                    "lat": lat,
                    "long": longi
                }
            }

            points.append(point)

        self.client.write_points(points)
