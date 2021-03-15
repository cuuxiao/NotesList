# -*- coding:utf-8 -*-
# @Time : 2021/3/15 16:55
# @Author: Truman
# @File : app.py

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "welcome to my notelist"
