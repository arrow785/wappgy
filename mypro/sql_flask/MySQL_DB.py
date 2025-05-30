# mysql的连接类

import pymysql
import pymysql.cursors


class ConMySQL:

    # 服务器 root@123
    def __init__(
        self, host="localhost", user="root", password="red9", port=3306, db_name="blog"
    ):
        self.host = host
        self.port = port
        self.password = password
        self.user = user
        self.db_name = db_name

    def getConnect(self):
        try:
            return pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db_name,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
            )
        except Exception as e:
            print("数据库连接失败")
            raise e
