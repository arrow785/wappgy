from sql_flask.mymysql import ConMySQL
from tools.mytools import get_time


# 根据id查询文章内容
def full_context(title_id: int, sqldb):
    sql = f"""
            select c.id,c.username,c.title,c.date,c.modify_date,c.contents from context as c where id = %s
        """
    c, cur = sqldb.mSQL()
    # 执行sql
    cur.execute(sql, (title_id,))
    result = cur.fetchone()
    print(f'==> {result},,id = {title_id}')
    return result


# 根据id查询评论
def by_id(title_id: int, sqldb):
    sql = f"""
            select d.username,d.comment_time,d.comment_context  from detailed as d where d.context_id = %s ORDER BY d.comment_time desc
        """
    c, cur = sqldb.mSQL()
    cur.execute(sql, (title_id,))
    return cur.fetchall()


# 写入评论
def insert_comment(name, comment_context, title_id, zhuti, sqldb):
    curr_time = get_time()
    sql = f"""
            insert into detailed(username,comment_time,comment_context,context_id,zhuti) values (%s,%s,%s,%s,%s)
        """
    c, cur = sqldb.mSQL()
    try:
        cur.execute(sql, (name, curr_time, comment_context, title_id, zhuti))
        c.commit()
    except Exception as e:
        print(f'未知错误！=> {e}')
    return cur.lastrowid
