# 这个文件会存放一些设置相关的配置信息
from flask import Flask


class SqlConfig:
    def __init__(self, db_name, host='127.0.0.1', port=3306, password='red9', user='root'):
        self.host = host
        self.port = port
        self.password = password
        self.user = user
        self.db_name = db_name

    def config(self):
        return {'host': self.host, 'port': self.port, 'password': self.password, 'user': self.user,
                'db_name': self.db_name}


class MyFlask():
    def __init__(self, app_name, host='127.0.0.1', port=5001):
        self.host = host
        self.port = port
        self.app = self.__getApp(app_name)
        self.mime_type = 'application/json'

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=True)

    def __getApp(self, flask_name):
        return Flask(flask_name)
