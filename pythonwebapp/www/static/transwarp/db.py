#!/usr/bin/python
# -*- coding: UTF-8 -*-
# db.py
import logging
import threading


# 数据库引擎对象:
class _Engine(object):
    def __init__(self, connect):
        self._connect = connect

    def connect(self):
        return self._connect()


engine = None


class _LasyConnection(object):
    def __init__(self):
        self.connection = None

    def cursor(self):
        if self.connection is None:
            _connection = engine.connection()
            logging.info('[CONNECTION] [OPEN] connection <%s>...' % hex(id(_connection)))
            self.connection = _connection
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
        if self.connection:
            _connection = self.connection
            self.connection = None
            logging.info('[CONNECTION] [CLOSE] connection <%s>...' % hex(id(_connection)))
            _connection.close()


# 数据库连接的上下文对象
class _DbCtx(threading.local):
    def __init__(self):
        self.connection = None
        self.transcations = 0

    def is_init(self):
        return not self.connection is None

    def init(self):
        self.connection = _LasyConnection
        self.transcations = 0

    def cleanup(self):
        self.connection.cleanup()

    def cursor(self):
        return self.connection.cursor()


_db_ctx = _DbCtx()


class _ConnextionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()


def connection():
    return _ConnextionCtx()


def select(sql, *args):
    pass
