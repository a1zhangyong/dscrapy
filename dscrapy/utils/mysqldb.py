#!/usr/bin/env python
# coding=utf-8
import MySQLdb as DB
import traceback

import log

class DBUtil:
    def __init__(self):
        self.inited = False
        
    def init(self, sHost, sUser, sPasswd, sDB, bPersist):
        if not self.inited:
            self.conn     = DB.connect(host=sHost, user=sUser, passwd=sPasswd, db=sDB, charset='utf8')
            self.persist  = bPersist
            self.inited   = True
    
    
    def execSql(self, sql, param):
        cur = self.conn.cursor()
        try:
            cur.execute(sql, param)
        finally:
            cur.close()

    def commit(self):
        self.conn.commit()
        """
        if  not self.persist:
            self.close()
        """
    
    def rollback(self):
        self.conn.rollback()
        """
        if  not self.persist:
            self.close()
        """
    
    def close(self):
        if self.inited:
            self.conn.close()
            self.inited = False
    
    
    def query(self,sql,display=True):
        """
            执行查询语句
        """
        if display :
            log.info(sql)
        
        cur = self.conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        
        return result
    
    def save_or_update(self,sql,display=True):
        """
            执行新增、更新、删除语句
        """
        if display :
            log.info(sql)
        try:
            self.execSql(sql, None)
            self.commit()
        except:
            traceback.format_exc()
            self.rollback()
            
    def get_insert_sql(self, obj, tb_name):
        field_str = ""
        value_str = ""
        fields = obj.__dict__.keys()
        for field in fields :
            value = getattr(obj, field)
            if value is None or value == "" :
                continue
            field_str += "%s," % field
            if type(value) == int or type(value) == float or type(value) == long :
                value_str += "%s," % value
            elif type(value) == str or type(value) == unicode :
                value_str += "\'%s\'," % value.replace("\'","\\\'")
            else :
                value_str += "\'%s\'," % value
        sql = "insert into %s(%s)values(%s)" % (tb_name,field_str.strip(","),value_str.strip(","))
        return sql

    def get_update_sql(self, obj, tb_name, condition_dict={}):
        """
                      需对象属性名和对应表字段名完全一样
         obj : 更新的对象
         tb_name : 对应表名称
         condition_dict : 条件,字典形式,只能实现等于条件 
        """
        
        where_str = " where "
        if not condition_dict :
            where_str = ""
        else :
            for key in condition_dict :
                value = condition_dict[key]
                if value is None or value == "" :
                    continue
                if type(value) == int or type(value) == float or type(value) == long :
                    where_str += "%s=%s and " % (key,value)
                elif type(value) == str or type(value) == unicode :
                    where_str += "%s=\'%s\' and " % (key,value.replace("\'","\\\'"))
                else :
                    where_str += "%s=\'%s\' and " % (key,value)
            where_str = where_str.strip(" and ")
        content = ""
        fields = obj.__dict__.keys()
        for field in fields :
            value = getattr(obj, field)
            if value is None or value == "" :
                continue
            if type(value) == int or type(value) == float or type(value) == long :
                content += "%s=%s," % (field,value)
            elif type(value) == str or type(value) == unicode :
                content += "%s=\'%s\'," % (field,value.replace("\'","\\\'"))
            else :
                content += "%s=\'%s\'," % (field,value)
        content = content.strip(",")
        sql = "update %s set %s %s" % (tb_name,content,where_str)
        return sql