#!/usr/bin/python
# -*- coding: UTF-8 -*-
# dbmodel.py
import MySQLdb

import constants
from dbmetaclass import ModelMetaClass

cur = None
conn = None


def create_engine():
    global conn
    conn = MySQLdb.connect(constants.host, constants.user, constants.password, constants.DATABASE_NAME, constants.port,
                           charset='utf8')
    global cur
    if cur is None:
        cur = conn.cursor()
    conn.autocommit(1)


def join_select(select_info):
    condition = ''
    if isinstance(select_info, dict):
        if len(select_info) > 0:
            for k in select_info.keys():
                if isinstance(select_info[k], str):
                    select_info[k] = '\'' + select_info[k] + '\''
                if condition is '':
                    condition = "%s=%s" % (k, select_info[k])
                else:
                    condition = condition + " and " + ("%s=%s" % (k, select_info[k]))
    else:
        condition = select_info
    return condition


# 所有Model类的基类
class Model(dict):
    __metaclass__ = ModelMetaClass

    def __init__(self, **kw):
        create_engine()
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    # 插入
    def insert(self, insert_info={}):
        fields = ''
        params = ''
        for k in insert_info.keys():
            if fields is '':
                fields = k
            else:
                fields += ',' + k
            if isinstance(insert_info[k], str):
                insert_info[k] = '\'' + insert_info[k] + '\''
            if params is '':
                params = str(insert_info[k])
            else:
                params += ',' + insert_info[k]
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, fields, params)
        print sql
        try:
            cur.execute(sql)
            conn.commit()
            return True
        except StandardError, e:
            print e
            print 'insert error happens'
            conn.rollback()

        return False

    # 完全自定义查询sql
    def selectmanual(self, sql=None):
        cur.execute(sql)
        result = cur.fetchall()
        return result

    # 查询
    def select(self, select_field, select_condition={}, order_by_dict={}, group_by_key=[]):
        sql = 'select %s from  %s' % (select_field, self.__table__)
        # 查询条件的拼接
        condition = join_select(select_condition)
        if condition is not '':
            sql += ' where ' + condition
        # 排序的拼接
        if isinstance(order_by_dict, dict):
            order_info = ''
            if len(order_by_dict) > 0:
                for k in order_by_dict.keys():
                    tag = ''
                    if order_by_dict[k] is True:
                        tag = 'asc'
                    else:
                        tag = 'desc'

                    if order_info is '':
                        order_info = '%s %s' % (k, tag)
                    else:
                        order_info += ',%s %s' % (k, tag)
            if order_info is not '':
                sql += ' order by %s' % order_info
        else:
            sql += ' order by %s' % order_by_dict
        # groupby信息的拼接，直接把需要groupby的字段全部存在一个list中
        if isinstance(group_by_key, list):
            if len(group_by_key) > 0:
                group_key = ''
                for v in group_by_key:
                    if group_key is '':
                        group_key = v
                    else:
                        group_key += ',' + v
                sql += " group by " + group_key
        else:
            sql += " group by " + str(group_by_key)
        print sql
        try:
            cur.execute(sql)
            result = cur.fetchall()
            return result
        except StandardError,e:
            print e
            return None

    # 更新
    def update(self, update_info={}, condition={}):
        sql = 'update %s' % self.__table__
        if len(update_info) > 0:
            update = ''
            if isinstance(update_info, dict):
                for k in update_info.keys():
                    if update is '':
                        update = '%s=%s' % (k, update_info[k])
                    else:
                        update = ',%s=%s' % (k, update_info[k])
            else:
                update = str(update_info)
            sql += 'set ' + update
        condition = join_select(condition)
        if condition is not '':
            sql += ' where ' + condition
        try:
            cur.execute(sql)
            return True
        except StandardError:
            conn.rollback()
            print 'update error happens'
        return False

    # 删除
    def delete(self, condition={}):
        sql = 'delete from %s' % self.__table__
        condition = join_select(condition)
        if condition is not '':
            sql += ' where ' + condition
        try:
            cur.execute(sql)
            return True
        except StandardError:
            conn.rollback()
            print 'delete error happens'
        return False
