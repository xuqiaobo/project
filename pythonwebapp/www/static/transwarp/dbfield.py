#!/usr/bin/python
# -*- coding: UTF-8 -*-
# dbfield.py

# 所有属性的基类
class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)


# 字符串属性类型
class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'string')


# 非字符串的属性类型
class OtherField(Field):
    def __init__(self, name):
        super(OtherField, self).__init__(name, 'other')
