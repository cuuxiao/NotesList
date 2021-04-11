# -*- coding:utf-8 -*-
# @Time : 2021/3/26 15:07
# @Author: Truman
# @File : __init__.py
import os
import sys

from flask import Flask
from flask_login import LoginManager, current_user
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
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, '../data.db')

# 关闭对模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

# os.getenv('SECRET_KEY', 'dev') 表示读取系统环境变量 SECRET_KEY 的值，如果没有获取到，则使用 dev
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))

# 在扩展类实例化化前加载配置
db = SQLAlchemy(app)
# ===============初始化登录用户===========================================================
login_manager = LoginManager(app)  # 实力化扩展类


# Flask-Login提供了一个current_user变量，注册这个函数后，如果用户已登录，current_user变量的值是当前用户的用户模型类记录
@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户ID作为参数
    from notesList.models import User
    user = User.query.get(int(user_id))  # 用ID作为User模型的主键查询对应用户
    return user


login_manager.login_view = 'login'
login_manager.login_message = 'Please login this website'


@app.context_processor
def inject_user():
    if current_user.is_authenticated:
        user = current_user
    else:
        from notesList.models import User
        user = User.query.first()
    # 需要返回字典，等同于return {‘user’： user}
    return dict(user=user)


from notesList import views, commands