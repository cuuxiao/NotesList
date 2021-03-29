# -*- coding:utf-8 -*-
# @Time : 2021/3/26 15:12
# @Author: Truman
# @File : views.py

from notesList import app, db
from notesList.models import Notes, User
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user


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
            flash('Invalid edit input.')
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
