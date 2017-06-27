#!/usr/bin/python
# -*- coding: UTF-8 -*-
# base.py
from app.models import User

u = User()
u.passsword = 'cat'
print u.password_hash
print u.verify_password('dof')
