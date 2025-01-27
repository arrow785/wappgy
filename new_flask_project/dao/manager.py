from sql_flask.mymysql import ConMySQL
from tools.mytools import get_time
connect, cursor = ConMySQL().mSQL()


def select_all_context(username: str,sqldb):
    sql = f"""
        SELECT * FROM context AS c
        WHERE c.username = %s
        ORDER BY c.date DESC
        """
    c,cur = sqldb.mSQL()
    cur.execute(sql, (username,))
    return cur.fetchall()


def update_content(title_id: int, content: str, title: str):
    sql = """
        UPDATE context
        SET contents = %s, title = %s, modify_date = %s
        FROM context
        WHERE id = %s
        """
    try:
        cursor.execute(sql, (content, title, get_time(), title_id))
        connect.commit()
    except Exception as e:
        print(e)
    return cursor.lastrowid

def find_context(title_id: int):
    sql = """
        SELECT * FROM context
        WHERE id = %s
        """
    cursor.execute(sql, (title_id,))
    return cursor.fetchone()

def delete_context(title_id: int):
    sql = """
        DELETE FROM context
        WHERE id = %s
        """
    try:
        cursor.execute(sql, (title_id,))
        connect.commit()
    except Exception as e:
        print(e)
    return cursor.lastrowid