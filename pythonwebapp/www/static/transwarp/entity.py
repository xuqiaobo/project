#!/usr/bin/python
# -*- coding: UTF-8 -*-
# entity.py
from dbmodel import Model


# 定义全部的实体类
class User(Model):
    __table__ = 'user'
    _fields = ('ID', 'name')

    def select(self, select_field='', select_condition={}, order_by_dict={}, group_by_key=[]):
        if select_field is '':
            for i in self._fields:
                if select_field is '':
                    select_field = i
                else:
                    select_field += ',' + i
        return super(User, self).select(select_field, select_condition, order_by_dict, group_by_key)
