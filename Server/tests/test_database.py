#!/usr/bin/python3

import unittest

from database import *


class TestDatabaseProxy(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabaseProxy, self).__init__(*args, **kwargs)
        self.db = database.Database()

    @unittest.skip
    def test_register(self):
        self.db.register({
            "username": "zonnax",
            "password": "ola",
            "name": "André Pedrosa",
            "email": "asdf@ua",
            "phpn": 111111113,
            "birth_date": "14-03-1998",
            "weight": 1.4,
            "height": 3.1,
            "additional_information": "doime cenas muitas vezes"
        })

    @unittest.skip
    def test_verifyUser(self):
        result = self.db.verifyUser({
            "username": "zonnax",
            "password": "ola"
        })
        self.assertTrue(result, "password ola")

        result = self.db.verifyUser({
            "username": "zonnax",
            "password": "olb"
        })
        self.assertFalse(result, "password olb")

    @unittest.skip
    def test_getAllUsers(self):
        print(self.db.getAllUsers())

    @unittest.skip
    def test_addDevice(self):
        self.db.addDevice(
            "zonnax",
            {
                "type": 2,
                "authentication_fields": {
                    "token":"cenas",
                    "refresh_token":"outras cenas"
                }
            }
        )
        self.db.addDevice(
            "zonnax",
            {
                "type": 1,
                "authentication_fields": {
                    "token": "asdflah34ohaohw",
                    "uuid": "112331",
                    "refresh_token": "asldfklksdjf34r34"
                },
                "latitude": 40.0344452345,
                "longitude": -8.23452345
            }
        )

    @unittest.skip
    def test_getAllDevices(self):
        print(self.db.getAllDevices("zonnax"))

    @unittest.skip
    def test_getSupportedDevices(self):
        print(self.db.getSupportedDevices())

    @unittest.skip
    def test_getData_args(self):
        print(self.db.getData("health_status", "zonnax", None, 1554714227, None))

    @unittest.skip
    def test_getData_sleep(self):
        print(self.db.getData("sleep", "zonnax", None, 1554662636, None))

    @unittest.skip
    def test_insert(self):
        print(self.db.insert("health_status", {
            "hearth_rate2": 60,
            "calories2": 50,
            "steps2": 10000
        }, "zonnax"))

    def test_insert_sleep(self):
        print(self.db.insert("sleep", {
            "day": 60,
            "duration": 50,
            "begin": 10000,
            "end": 10000,
            "sleep": {
                "time": [],

            }
        }, "zonnax"))

    @unittest.skip
    def test_get_user_profile(self):
        print(self.db.getProfile("aspedrosa"))

    @unittest.skip
    def test_update_user_profile(self):
        self.db.updateProfile(
            "aspedrosa",
            {
                "password": "ola",
                "name": "André Pedrosa",
                "email": "asdf@ua",
                "phpn": 111111112,
                "birth_date": "2019-03-04",
                "weight": 1.4,
                "height": 3.1,
                "diseases": "doime cenas muitas vezes"
            }
        )


if __name__ == '__main__':
    unittest.main()