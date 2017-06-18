#!/usr/bin/python
# -*- coding: UTF-8 -*-
# dbconnection.py

import MySQLdb
import constants


class Connection(object):
    __connection = None

    @staticmethod
    def get_connection():
        if Connection.__connection is None:
            Connection.__connection = MySQLdb.connect(constants.host, constants.user, constants.password,
                                                      constants.DATABASE_NAME, constants.port,
                                                      charset='utf8')
            return Connection.__connection

    @staticmethod
    def close_connection():
        if Connection.__connection is not None:
            Connection.__connection.close()
