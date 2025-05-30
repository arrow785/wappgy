from sql_flask.MySQL_DB import ConMySQL
from Tools import get_time

newConMysql = ConMySQL()


def select_all_context(username):
    sql = f"""
        SELECT * FROM context AS c
        WHERE c.username = %s
        ORDER BY c.date DESC
        """

    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (username,))
        res = cur.fetchall()
        return res if res else []


def update_content(title_id, content, title, type_id):
    sql = """
            UPDATE context
            SET contents = %s, title = %s, modify_date = %s, typeid = %s
            WHERE id = %s
            """
    with newConMysql.getConnect() as db:
        cursor = db.cursor()
        cursor.execute(sql, (content, title, get_time(), type_id, title_id))
        db.commit()
        res = cursor.rowcount
        return res if res else 0


def find_context(title_id: int):
    sql = """
        SELECT * FROM context
        WHERE id = %s
        """
    with newConMysql.getConnect() as db:
        cursor = db.cursor()
        cursor.execute(sql, (title_id,))
        res = cursor.fetchone()
        return res if res else None


def delete_context(title_id: int):
    sql = """
        DELETE FROM context
        WHERE id = %s
        """
    with newConMysql.getConnect() as db:
        cursor = db.cursor()
        cursor.execute(sql, (title_id,))
        db.commit()
        res = cursor.rowcount
        return res if res else 0


def getTypeName(type_id):
    sql = """
        SELECT d.explain as `type_name` FROM article_type as d
        WHERE typeid = %s
    """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (type_id,))
            res = cursor.fetchone()
            return res["type_name"] if res else 0
    except Exception as e:
        print("error: ", e)
        return 0
    finally:
        print("getTypeName() finally 释放链接")
