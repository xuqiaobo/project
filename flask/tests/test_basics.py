#!/usr/bin/python
# -*- coding: UTF-8 -*-
# test_basics.py

import unittest

from flask import current_app

from app import create_app
from app import db


class BasicsTestCase(unittest.TestCase):
    # 测试用例开始之前执行的操作
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # 测试用例执行之后所要执行的操作
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exsits(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
