from sql_flask.mymysql import ConMySQL

connect, cursor = ConMySQL().mSQL()


# 展示所有数据
def select_all(page, sqldb, per_page=5, ):
    offset = (page - 1) * per_page
    sql = f"SELECT * FROM context AS c ORDER BY c.date DESC LIMIT %s OFFSET %s"
    c, cur = sqldb.mSQL()
    cur.execute(sql, (per_page, offset))
    result = cur.fetchall()
    return result


# 获取总文章数
def get_total_articles(sqldb):
    c, cur = sqldb.mSQL()
    sql = "SELECT COUNT(*) AS total FROM context"
    cur.execute(sql)
    result = cur.fetchone()
    return result['total']
