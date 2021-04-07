# -*- coding:utf-8 -*-
# @Time : 2021/4/7 10:20
# @Author: Truman
# @File : wsgi.py.py

import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from notesList import app
