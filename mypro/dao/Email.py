from sql_flask.MySQL_DB import ConMySQL
from Tools import get_time

newConMysql = ConMySQL()


def insert_email(username, email, content):
    curr_time = get_time()
    sql = f"""
            insert into email(send_username,send_email,send_content,send_date,is_send) values (%s,%s,%s,%s,'失败')
        """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (username, email, content, curr_time))
        db.commit()
        res = cur.rowcount
        return res if res else 0


def update_emial(username):
    sql = f"""update email set is_send = '成功' where send_username = %s"""
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (username,))
        db.commit()
        res = cur.rowcount
        return res if res else 0


def select_emial(username):
    sql = f"""select * from email where send_username = %s"""
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (username,))
        res = cur.fetchall()
        return res if res else []


def em_dy_data_(email_page, limit, username):
    offset = (email_page - 1) * limit
    sql = """
        select * from email where send_username = %s limit %s offset %s
    """
    with newConMysql.getConnect() as db:
        cursor = db.cursor()
        cursor.execute(sql, (username, limit, offset))
        results = cursor.fetchall()
        return results if results else []
