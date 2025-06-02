# 这个文件会存放一些设置相关的配置信息
from flask import Flask


class MyFlask:
    def __init__(self, app_name, host="127.0.0.1", port=5002, debug=True):
        self.host = host
        self.appName = app_name
        self.port = port
        self.mime_type = "application/json"
        self.debug = debug
        self.app = self.__getApp__(app_name)

    def run(self):
        # 运行Flask应用
        self.app.run(host=self.host, port=self.port, debug=self.debug)

    def __getApp__(self, appName):
        return Flask(appName, template_folder="templates", static_folder="static")
