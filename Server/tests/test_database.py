#!/usr/bin/python3

import unittest
import datetime

from pprint import pprint

from database import *

class TestDatabaseProxy(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabaseProxy, self).__init__(*args, **kwargs)
        self.db = database.Database()

    @unittest.skip
    def test_register(self):
        self.db.register({
            "type": "client",
            "username": "aspedrosa2",
            "password": "ola",
            "name": "André Pedrosa",
            "email": "asdf@ua",
            "phpn": 236457836,
            "birth_date": "14-03-1998",
            "weight": 1.4,
            "height": 3.1,
            "additional_information": "doime cenas muitas vezes"
        })
        self.db.register({
            "type": "doctor",
            "username": "arnaldo",
            "password": "ola",
            "name": "André Pedrosa",
            "email": "asdf@ua",
            "company": None,
            "specialities": "14-03-1998"
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
    def test_updateProfile(self):
        self.db.updateProfile("aspedrosa2", {
            "type": "client",
            "password": "ola",
            "name": "André Pedrosa 2",
            "email": "asdf@ua",
            "phpn": 236457836,
            "birth_date": "14-03-1998",
            "weight": None,
            "height": None,
            "additional_information": "doime cenas poucas vezes"
        })
        self.db.updateProfile("arnaldo", {
            "type": "doctor",
            "password": "ola",
            "name": "Arnaldo Pedrosa",
            "email": "asdf@ua",
            "company": None,
            "specialities": None
        })

    @unittest.skip
    def test_getProfile(self):
        pprint(self.db.getProfile("aspedrosa2"))
        pprint(self.db.getProfile("arnaldo"))

    @unittest.skip
    def test_getAllUsers(self):
        print(self.db.getAllUsers())

    @unittest.skip
    def test_addDevice(self):
        self.db.addDevice(
            "zonnax",
            {
                "type": "Foobot ",
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
    def test_updateDevice(self):
        self.db.updateDevice("zonnax", {
            "id": 10,
            "refresh_token": "outrascenas",
            "token": "outrascenas3",
            "latitude": 1,
            "longitude": 1,
        })

    @unittest.skip
    def test_deleteDevice(self):
        self.db.deleteDevice("zonnax", 3)

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
    def test_getDataByMedic(self):
        print(self.db.getDataByMedic("medic", "health_status", "zonnax", 1555781567, None, None))

    @unittest.skip
    def test_getData_sleep(self):
        print(self.db.getData("sleep", "zonnax", 1554662636, None, None))

    @unittest.skip
    def test_insert(self):
        print(self.db.insert("health_status", {
            "time": 1555781667,
            "hearth_rate": 60,
            "calories": 50,
            "steps": 10000
        }, "zonnax"))

    @unittest.skip
    def test_insert_sleep(self):
        print(self.db.insert("sleep", {
            "day": "2019-04-07",
            "duration": 39600,
            "begin": 1554679800,
            "end": 1554710400,
            "sleep": [
                {
                    "time": 1554679800,
                    "level": "awake",
                    "duration": 120
                },
                {
                    "time": 1554679920,
                    "level": "rest",
                    "duration": 39420
                },
                {
                    "time": 1554719340,
                    "level": "restless",
                    "duration": 60
                }
            ]
        }, "zonnax"))

    @unittest.skip
    def test_requestPermission(self):
        print(self.db.requestPermission("medic", {
            "username":"fpyjdd88888888",
            "health_number": None,
            "duration": 2
        }))

    @unittest.skip
    def test_deleteRequestPermission(self):
        self.db.deleteRequestPermission("medic", "zonnax")

    @unittest.skip
    def test_grantPermission(self):
        self.db.grantPermission("zonnax", "medic", 3)

    @unittest.skip
    def test_acceptPermission(self):
        self.db.acceptPermission("zonnax", "medic")

    @unittest.skip
    def test_deleteAcceptedPermission(self):
        self.db.deleteAcceptedPermission("zonnax", "medic")

    @unittest.skip
    def test_rejectPermission(self):
        self.db.rejectPermission("zonnax", "medic")

    @unittest.skip
    def test_hasPermission(self):
        print(self.db.relational_proxy.has_permission("medic", "zonnax"))

    @unittest.skip
    def test_stopAcceptedPermission(self):
        self.db.stopAcceptedPermission("medic", "zonnax")

    @unittest.skip
    def test_removeAcceptedPermission(self):
        self.db.removeAcceptedPermission("zonnax", "medic")

    @unittest.skip
    def test_getHistoricalPermissions(self):
        print(self.db.getHistoricalPermissions("zonnax"))
        print(self.db.getHistoricalPermissions("medic"))

    @unittest.skip
    def test_allPermissionsData(self):
        print(self.db.allPermissionsData("zonnax"))
        print(self.db.allPermissionsData("medic"))

if __name__ == '__main__':
    unittest.main()
