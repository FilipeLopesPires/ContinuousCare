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
            "username": "aspedrosa",
            "password": "ola",
            "name": "André Pedrosa",
            "email": "asdf@ua",
            "phpn": 111111111,
            "birth_date": "2019-03-04",
            "weight": 1.4,
            "height": 3.1,
            "diseases": [
                "doime cenas",
                "outras cenas"
            ]
        })

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


if __name__ == '__main__':
    unittest.main()
