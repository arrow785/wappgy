from Tools import get_time
from sql_flask.MySQL_DB import ConMySQL


newConMysql = ConMySQL()


# 根据id查询文章内容
def full_context(title_id: int):
    sql = f"""
            	select a.avatar,c.id,c.username,c.title,c.date,c.modify_date,c.contents,a.nick_name,d.typeid,d.`explain` from context as c 
               RIGHT  join users as a
            on a.username = c.username
						RIGHT JOIN article_type as d
						on d.id = c.typeid
            where c.id = %s
        """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (title_id,))
        result = cur.fetchone()
        return result if result else {}


# 获取收藏数
def getStarNumber(title_id):
    sql = """
        SELECT count(*) number FROM starbook AS s WHERE s.content_id = %s
    """
    with newConMysql.getConnect() as db:
        cursor = db.cursor()
        cursor.execute(sql, (title_id,))
        res = cursor.fetchone()
        return res["number"] if res else 0


# 根据id查询评论数
def by_id_get_comments(title_id: int):
    sql = """
            select count(*) as `numbers` from comments as c
                join users as a
            on a.username = c.username
            where c.context_id = %s
			GROUP BY c.context_id

           
        """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (title_id))
        comments = cur.fetchone()
        return comments["numbers"] if comments else 0


# 分页查询评论
def by_id_get_comments_fy_data(page, limit, titleid):
    offset = (page - 1) * limit
    sql = """
        select a.avatar,c.id,c.username,c.comment_time,c.comment_context,c.context_id,c.zhuti,a.nick_name from comments as c
                join users as a
            on a.username = c.username
            where c.context_id = %s
			ORDER BY c.comment_time DESC
            LIMIT %s OFFSET %s
    """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (titleid, limit, offset))
        res = cur.fetchall()
        return res if res else []


# 写入评论
def insert_comment(name, comment_context, title_id, zhuti):
    curr_time = get_time()
    sql = f"""
            insert into comments(username,comment_time,comment_context,context_id,zhuti) values (%s,%s,%s,%s,%s)
        """

    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (name, curr_time, comment_context, title_id, zhuti))
        db.commit()
        res = cur.rowcount
        return res if res else False


# 获取当前作者的最新三条动态
def getLatestArticleByUsername(username):
    sql = """
        select c.title,c.contents,c.date,c.id from context as c 
                join users as a
            on a.username = c.username
						WHERE c.username = %s
						ORDER BY c.date DESC
						limit 3 OFFSET 0;
    """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (username))
        res = cur.fetchall()
        return res if res else []
