# mysql的连接类

import pymysql
import pymysql.cursors

# 使用连接池
from dbutils.pooled_db import PooledDB


class ConMySQL:

    # 服务器 root@123
    def __init__(
        self,
        host="localhost",
        user="root",
        password="red9",
        port=3306,
        db_name="blog",
        pool_size=9,
    ):
        self.host = host
        self.port = port
        self.password = password
        self.user = user
        self.db_name = db_name
        self.poool = PooledDB(
            creator=pymysql,
            maxconnections=pool_size,
            mincached=2,  # 创建连接时，初始化连接数
            maxcached=3,
            blocking=True,  # 阻塞连接，当连接数达到最大时，后续连接请求会阻塞
            ping=0,  # 检测连接是否可用
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db_name,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def getConnect(self):
        try:
            return self.poool.connection()
        except Exception as e:
            print("数据库连接失败")
            raise e
