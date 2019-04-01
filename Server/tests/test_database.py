#!/usr/bin/python3

import unittest

from database import *


class TestDatabaseProxy(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabaseProxy, self).__init__(*args, **kwargs)
        self.db = database.Database()

    @unittest.skip
    def test_insert_user(self):
        self.db.register({
            "username": "zonnax",
            "password": "ola",
            "name": "André Pedrosa",
            "email": "asdf@ua",
            "phpn": 111111113,
            "birth_date": "2019-03-04",
            "weight": 1.4,
            "height": 3.1,
            "diseases": "doime cenas muitas vezes"
        })

    @unittest.skip
    def test_verify_credentials(self):
        result = self.db.verifyUser({
            "username": "aspedrosa",
            "password": "ola"
        })
        self.assertTrue(result, "password ola")

        result = self.db.verifyUser({
            "username": "aspedrosa",
            "password": "olb"
        })
        self.assertFalse(result, "password olb")

    @unittest.skip
    def test_insert_device(self):
        self.db.addDevices(
            "aspedrosa",
            {
                "type": 1,
                "token": "asdffghj"
            }
        )

    @unittest.skip
    def test_get_all_client_devices(self):
        print(self.db.getAllDevices("aspedrosa"))

    @unittest.skip
    def test_get_all_supported_devices(self):
        print(self.db.getSupportedDevices())

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

    def test_all_metrics(self):
        print(self.db._get_all_environment_metrics())


if __name__ == '__main__':
    unittest.main()
