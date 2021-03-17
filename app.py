# -*- coding:utf-8 -*-
# @Time : 2021/3/15 16:55
# @Author: Truman
# @File : app.py

import os
import sys

from flask import Flask, render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# 实例初始化
app = Flask(__name__)
# 配置数据连接地址
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# 关闭对模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 在扩展类实例化化前加载配置
db = SQLAlchemy(app)

#表名将会是user，自动生成，小写处理
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)    #主键
    name = db.Column(db.String(20))                 #名字

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tile = db.Column(db.String(60))
    notes = db.Column(db.String(20))

name = 'Truman'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

@app.route('/')
def index():
    return render_template('index.html', name = name, movies = movies)

@app.route('/home')
@app.route('/index')
def hello():
    return '<h1>hello Truman!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return 'User : %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name = 'truman'))
    print(url_for('user_page', name = 'peter'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num = 2))
    return  'Test page'