#!/usr/bin/python
# -*- coding: UTF-8 -*-
# models.py
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))
# Flask必须指定一个参数，即程序主模块或包的名字
server = Flask(__name__)
server.config['SECRET_KEY'] = 'hard to guess string'
server.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
server.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(server)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def passsword(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
