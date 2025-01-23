# mysql的连接类

import pymysql as mysql
from sql_flask.settings import SqlConfig


class ConMySQL:
    def __init__(self):
        conf = SqlConfig(db_name='blog')
        self.__conf = conf.config()

    def mSQL(self):
        return self.__getLink()

    def __getLink(self):
        try:
            connect = mysql.connect(host=self.__conf['host'],
                                    port=self.__conf['port'],
                                    user=self.__conf['user'],
                                    password=self.__conf['password'],
                                    db=self.__conf['db_name'],
                                    charset='utf8mb4')
            cursor = connect.cursor(mysql.cursors.DictCursor)
            return connect, cursor
        except Exception as e:
            print(f"连接数据库失败，错误详细：{e}")
