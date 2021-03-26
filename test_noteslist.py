# -*- coding:utf-8 -*-
# @Time : 2021/3/26 11:13
# @Author: Truman
# @File : test_noteslist.py

import unittest
from app import app, db, User, Notes


class NotesListTestCase(unittest.TestCase):

    def setUp(self):
        print('=========== Start setup ===========')
        # 更新配置
        app.config.update(
            # 开启测试模式，这样在出错时不会输出多余信息
            TESTING=True,
            # 'sqlite:///:memory:' 是SQLite内存型数据库，不会干扰开发时使用的数据库文件
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        # 创建数据库和表
        db.create_all()
        # 创建测试数据，一个用户，一个笔记条目
        user = User(type='Test', username='test')
        user.set_password('123')
        notes = Notes(title='title test', content='content test', link='link test', owner='Test')
        # 使用add_all()方法一次添加多个模型类实例，传入列表
        db.session.add_all([user, notes])
        db.session.commit()

        self.client = app.test_client()  # 创建测试客户端，模拟客户端请求
        self.runner = app.test_cli_runner()  # 创建测试命令运行器，触发自定义命令

    def tearDown(self):
        print('=========== Start tearDown ===========')
        db.session.remove()  # 清除数据库会话
        db.drop_all()  # 删除数据库

    # 测试程序实例是否存在
    def test_app_exist(self):
        print('=========== Start test_app_exist ===========')
        self.assertIsNotNone(app)

    # 测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    # 测试404页面
    def test_404_page(self):
        print('=========== Start test_404_page ===========')
        response = self.client.get('/nothing')  # 传入目标URL
        # as_text 参数设为 True 可以获取 Unicode 格式的响应主体
        data = response.get_data(as_text=True)
        self.assertIn('Page Not Found - 404', data)
        self.assertEqual(response.status_code, 404)  # 判断想要状态码

    # 测试主页
    def test_index_page(self):
        print('=========== Start test_index_page ===========')
        self.login()
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('test\'s Noteslist', data)
        self.assertIn('Add Notes', data)
        self.assertEqual(response.status_code, 200)

    """
    # app.test_client() 返回一个测试客户端对象，可以用来模拟客户端（浏览器），我们创建类属性 self.client 来保存它
    # 对它调用 get() 方法就相当于浏览器向服务器发送 GET 请求，调用 post() 则相当于浏览器向服务器发送POST 请求
    """

    # 辅助方法，用户登录用户
    def login(self):
        self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)
        # follow_redirects 参数设为 True 可以跟随重定向，最终返回的会是重定向后的响应。


if __name__ == '__main__':
    unittest.main()
