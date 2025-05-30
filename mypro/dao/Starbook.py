from sql_flask.MySQL_DB import ConMySQL


newConMysql = ConMySQL()


# 该用户是否收藏
def isStarBook(username: str, content_id):
    print(f"isStarBook() ==>  {username} content_id => {content_id}")
    sql = """
        SELECT s.content_id,COUNT(*) FROM starbook AS s
        left JOIN users AS a1 
        on a1.id = s.content_id
				WHERE s.login_name = %s and s.content_id = %s
				GROUP BY s.content_id
        """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(
            sql,
            (
                username,
                content_id,
            ),
        )
        rs = cur.fetchone()
        return rs if rs else None


# 收藏
def star_book(id, login_name):
    sql = "insert into starbook(content_id,login_name) values(%s,%s)"
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(
            sql,
            (
                id,
                login_name,
            ),
        )
        db.commit()
        res = cur.rowcount
        return res if res else 0


def cancel_star_book(content_id, login_name):
    sql = """
        DELETE FROM starbook WHERE content_id = %s AND login_name = %s
    """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (content_id, login_name))
        db.commit()
        res = cur.rowcount
        return res if res else 0
