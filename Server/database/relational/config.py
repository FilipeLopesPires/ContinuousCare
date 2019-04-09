#!/usr/bin/python3

"""
Information to create a connection to the database

Because this file contains critical/important information it is
advised to change the permissions on this file

chmod 600 config.py
"""

HOST      = "localhost"
PORT      = 3306
USERNAME  = "pi2019cc_flaskapp"
PASSWORD  = "T)[-keLSh.9UFZcN58.+"
DATABASE  = "db"
POOL_NAME = "flaskapp_conenction_pool"
POOL_SIZE = 10 #TODO search error "to many connections"
