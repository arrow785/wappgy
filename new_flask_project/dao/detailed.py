from tools.mytools import get_time


# 根据id查询文章内容
def full_context(title_id: int, sqldb):
    c, cur = sqldb.mSQL()
    sql = f"""
            select a.avatar,c.id,c.username,c.title,c.date,c.modify_date,c.contents from context as c 
                join admin as a
            on a.username = c.username
            where c.id = %s;
        """
    try:

        cur.execute(sql, (title_id,))
        result = cur.fetchone()
        print(f'==> {result},,id = {title_id}')
        return result
    except Exception as e:
        print(f'根据id查询文章内容 full_context() 错误！=> {e}')
        c.rollback()


# 根据id查询评论
def by_id(title_id: int, sqldb):
    sql = f"""
           select a.avatar,c.id,c.username,c.comment_time,c.comment_context,c.context_id,c.zhuti from detailed as c
                join admin as a
            on a.username = c.username
            where c.context_id = %s
			ORDER BY c.comment_time DESC
        """
    try:
        c, cur = sqldb.mSQL()
        cur.execute(sql, (title_id,))
        comments = cur.fetchall()
        return comments
    except Exception as e:
        print(f'根据id查询评论 by_id() 错误！=> {e}')


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
        print(f' insert_comment() 写入评论错误！=> {e}')
    return cur.lastrowid
