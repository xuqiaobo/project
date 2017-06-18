#!/usr/bin/python
# -*- coding: UTF-8 -*-
from entity import User


u=User()
# 保存到数据库：
sql = u.select()
print sql
