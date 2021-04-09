# -*- coding:utf-8 -*-
# @Time : 2021/3/26 15:12
# @Author: Truman
# @File : commands.py

import click

from notesList import app, db
from notesList.models import User


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
