from sql_flask.mymysql import ConMySQL
from tools.mytools import get_time

connect, cursor = ConMySQL().mSQL()


def insert_context(title, contents, username):
    current_time = get_time()
    sql = f"""
            insert into context(title,username,contents,date) values (%s,%s,%s,%s)
        """
    try:
        cursor.execute(sql, (title, username, contents, current_time))
        connect.commit()
    except Exception as e:
        print(f'未知错误！=> {e}')
    return cursor.lastrowid
