# -*- coding:utf-8 -*-
# @Time : 2021/3/26 15:12
# @Author: Truman
# @File : models.py

from notesList import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# ===============建立数据模型===========================================================
"""
# 表名将会是user，自动生成，小写处理， 
# 继承UserMixin这个类会让 User 类拥有几个用于判断认证状态的属性和方法，其中最常用的是is_authenticated 属性：
# 如果当前用户已经登录，那么current_user.is_authenticated会返回True,否则返回 False
"""


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    type = db.Column(db.String(20))  # 名字
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    # 用来设置密码的方法，接受密码作为参数
    def set_password(self, password):
        # 将生成的密码保存到对应字段
        self.password_hash = generate_password_hash(password)

    # 用于验证密码的方法，接受密码作为参数
    def validate_password(self, password):
        # 返回布尔值
        return check_password_hash(self.password_hash, password)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    content = db.Column(db.String(20))
    link = db.Column(db.String(30))
    owner = db.Column(db.String(20))
    comments = db.Column(db.String(20))
    reserved1 = db.Column(db.String(20))
    reserved2 = db.Column(db.String(20))
    reserved3 = db.Column(db.String(20))
