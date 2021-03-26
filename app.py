# -*- coding:utf-8 -*-
# @Time : 2021/3/15 16:55
# @Author: Truman
# @File : app.py

import os
import sys

from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import click
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

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

# ===============初始化登录用户===========================================================
login_manager = LoginManager(app)  # 实力化扩展类
login_manager.login_view = 'login'
login_manager.login_message = 'Please login this website'


# FLask-Login提供了一个current_user变量，注册这个函数后，如果用户已登录，current_user变量的值是当前用户的用户模型类记录
@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户ID作为参数
    user = User.query.get(int(user_id))  # 用ID作为User模型的主键查询对应用户
    return user


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


# ===============注册命令===========================================================
@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
        click.echo('drop the database. ')  # 输出提示信息
    db.create_all()
    click.echo('Initialized database. ')  # 输出提示信息


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login. ')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login. ')
def admin(username, password):
    """Create admin user. """
    db.create_all()

    # new 新方法，针对多用户，判断用户是否存在，存在就更新，不存在则创建
    user = User.query.filter(User.username == username).first()
    if user:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, type='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done..')

    # 2222 创建用户，并判断用户是否存在；如果新增用户存在，则更新密码；如果用户不存在，则增加用户
    # user = User.query.all()
    # if user:
    #     for i in range(len(user)):
    #         if user[i].username == username:
    #             click.echo('Updating user...')
    #             user[i].username = username
    #             user[i].set_password(password)  # 设置密码
    #             break
    #         elif i == len(user)-1 and user[i].username != username:
    #             click.echo('Adding user...')
    #             user = User(username=username, type='Admin')
    #             user.set_password(password)
    #             db.session.add(user)
    # else:
    #     click.echo('Creating user...')
    #     user = User(username=username, type='Admin')
    #     user.set_password(password)
    #     db.session.add(user)

    # 11111 原始方法，针对一个用户，判断用户是否存在，存在就更新，不存在则创建
    # if user is not None:
    #     click.echo('Updating user...')
    #     user.username = username
    #     user.set_password(password)  # 设置密码
    # else:
    #     click.echo('Creating user...')
    #     user = User(username=username, type='Admin')
    #     user.set_password(password)
    #     db.session.add(user)

    # db.session.commit()
    # click.echo('Done..')


# ================== web程序 ===============================================================

@app.route('/')
@login_required  # 用户视图保护,认证保护
def index():
    # if not current_user.is_authenticated:
    #     return redirect(url_for('login'))
    query_result = Notes.query.filter(Notes.owner == current_user.username).all()
    return render_template('index.html', notes=query_result)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid username or passcode. ')
            return redirect(url_for('login'))

        user = User.query.filter(User.username == username).first()
        if user and user.validate_password(password):
            login_user(user)    # 登入用户
            flash('Welcome ' + current_user.username + ' to login. ')
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or passcode. ')
            return redirect(url_for('login'))

        # user = User.query.first()
        # # 验证用户名和密码是否一致
        # if username == user.username and user.validate_password(password):
        #     login_user(user)                        # 登入用户
        #     flash('Login success. ')
        #     return redirect(url_for('index'))
        #
        # flash('Incorrect username or passcode. ')
        # return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required  # 用户视图保护,认证保护
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.......')
    return redirect(url_for('index'))


@app.route('/notes/add', methods=['GET', 'POST'])
@login_required  # 登录保护
def add():
    if request.method == 'POST':
        # 获取表单数据
        title = request.form.get('title')
        content = request.form.get('content')
        link = request.form.get('link')
        owner = current_user.username

        if not title or not content or len(link) > 30 or len(content) > 20 or len(title) > 20:
            flash('Invalid input.')  # 显示错误信息
            return redirect(url_for('add'))  # 重定向回主页

        notes = Notes(title=title, content=content, link=link, owner=owner)
        db.session.add(notes)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/notes/edit/<int:notes_id>', methods=['GET', 'POST'])
@login_required  # 登录保护
def edit(notes_id):
    notes = Notes.query.get_or_404(notes_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        link = request.form['link']
        owner = current_user.username

        if not title or not content or len(link) > 30 or len(content) > 20 or len(title) > 20:
            flash('Inavelid edit input.')
            return redirect(url_for('edit', notes_id=notes_id))  # 重定向对应的编辑页面

        notes.title = title
        notes.content = content
        notes.link = link
        notes.owner = owner
        db.session.commit()
        flash('Item updated. ')
        return redirect(url_for('index'))
    return render_template('edit.html', notes=notes)


@app.route('/notes/delete/<int:notes_id>', methods=['POST'])  # 只接受POST请求
@login_required  # 登录保护
def delete(notes_id):
    notes = Notes.query.get_or_404(notes_id)  # 获取笔记记录
    db.session.delete(notes)
    db.session.commit()  # 提交数据库会话
    flash('Item deleted. ')
    return redirect(url_for('index'))  # 重定向回主页


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        username = request.form['username']

        if not username or len(username) > 20:
            flash('Invalid username. ')
            return redirect(url_for('settings'))

        # current_user会返回当前登录用户的数据库记录对象,等同于下面的用法
        # user = User.query.first()
        # user.username = username
        current_user.username = username
        db.session.commit()
        flash('Settings updated done')
        return redirect(url_for('index'))
    return render_template('settings.html')


@app.errorhandler(404)  # 传入需要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    flash('Page Not Found - 404')
    return render_template('404.html'), 404  # 返回模板和状态码


@app.context_processor
def inject_user():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = User.query.first()

    return dict(user=user)  # 需要返回字典，等同于return {‘user’： user}
