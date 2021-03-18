# -*- coding:utf-8 -*-
# @Time : 2021/3/15 16:55
# @Author: Truman
# @File : app.py

import os
import sys

from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import click

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# 实例初始化
app = Flask(__name__)
# 配置数据连接地址
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
# 关闭对模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 在扩展类实例化化前加载配置
db = SQLAlchemy(app)

#表名将会是user，自动生成，小写处理
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # 主键
    name = db.Column(db.String(20))                 # 名字

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    note = db.Column(db.String(20))

@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
    # 设置选项
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
        click.echo('drop the database. ')  # 输出提示信息
    db.create_all()
    click.echo('Initialized database. ')    # 输出提示信息

@app.route('/')
def index():
    user = User.query.first()
    notes = Notes.query.all()
    return render_template('index.html', name = user.name, movies = notes)

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
    return 'Test page'