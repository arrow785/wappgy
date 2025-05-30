from sql_flask.MySQL_DB import ConMySQL


newConMysql = ConMySQL()


def getNickName(username):
    sql = "SELECT nick_name FROM users WHERE username = %s"
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (username,))
        res = cur.fetchone()
        return res["nick_name"] if res else "d"


# 展示所有数据
def select_all_content(limit, current_page):
    offset = (current_page - 1) * limit
    sql = """
    SELECT c.id,c.username, s.nick_name,c.contents,c.date FROM context AS c 
        LEFT JOIN users as s
        on s.username = c.username
        ORDER BY c.date DESC LIMIT %s OFFSET %s;
    """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (limit, offset))
        result = cur.fetchall()
        return result if result else []


def select_all(
    limit,
    offset=3,
):
    offset = (offset - 1) * limit
    sql = f"""
    SELECT c.id,c.username, s.nick_name,c.title,c.date FROM context AS c 
            LEFT JOIN users as s
            on s.username = c.username
            ORDER BY c.date DESC LIMIT %s OFFSET %s
    """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (limit, offset))
        result = cur.fetchall()
        return result if result else []


def select_all_context(username):
    if username == "d":
        print("未知用户！")
        return None
    sql = f"""
        SELECT * FROM context AS c
        WHERE c.username = %s
        ORDER BY c.date DESC
        """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (username,))
        res = cur.fetchone()
        return res if res else None


# 获取总文章数
def get_total_articles(typeid=0):

    sql = "SELECT COUNT(*) AS total FROM context"
    if typeid != 0:
        sql = """SELECT COUNT(*) AS total FROM context WHERE typeid = %s"""
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        if typeid != 0:
            cur.execute(sql, (typeid,))
        else:
            cur.execute(sql)
        result = cur.fetchone()
        return result["total"] if result else 0
