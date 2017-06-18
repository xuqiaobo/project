#!/usr/bin/python
# -*- coding: UTF-8 -*-
# dbmetaclass.py
from dbfield import Field


# 元祖类
class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                print ("Found mapping:%s==%s" % (k, v))
                mappings[k] = v
        for k in mappings.iterkeys():
            attrs.pop(k)

        attrs['__table__'] = name.lower()
        attrs['__mappings__'] = mappings

        return type.__new__(cls, name, bases, attrs)
