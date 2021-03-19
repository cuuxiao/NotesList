# -*- coding:utf-8 -*-
# @Time : 2021/3/15 16:55
# @Author: Truman
# @File : app.py

import os
import sys

from flask import Flask, render_template, request, redirect, flash, url_for
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
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)

# 在扩展类实例化化前加载配置
db = SQLAlchemy(app)


# 表名将会是user，自动生成，小写处理
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    comments = db.Column(db.String(20))
    link = db.Column(db.String(20))


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
        click.echo('drop the database. ')  # 输出提示信息
    db.create_all()
    click.echo('Initialized database. ')  # 输出提示信息


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取表单数据
        title = request.form.get('title')
        comments = request.form.get('comments')
        link = request.form.get('link')
        # 判断数据是否符合要求
        if not title or not comments or len(comments) > 20 or len(title) > 20:
            flash('Invalid input.')                 # 显示错误信息
            return redirect(url_for('index'))       # 重定向回主页
        # 保存表单数据到数据库
        notes = Notes(title=title, comments=comments, link=link)
        db.session.add(notes)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))
    comments = Notes.query.all()
    return render_template('index.html', comments=comments)


@app.errorhandler(404)  # 传入需要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html'), 404  # 返回模板和状态码


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于return {‘user’： user}