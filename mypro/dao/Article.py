from sql_flask.MySQL_DB import ConMySQL
from Tools import get_time

newConMysql = ConMySQL()


# 插入文章
def insert_article(title, contents, username, type_id, cover_path):

    current_time = get_time()
    sql = """
            insert into 
            article(title,username,contents,date,typeid,cover_url,likes_number) 
            values (%s,%s,%s,%s,%s,%s,0)
        """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(
                sql,
                (
                    title,
                    username,
                    contents,
                    current_time,
                    type_id,
                    cover_path,
                ),
            )
            res = cursor.lastrowid  # 获取插入的最后一条记录的ID
            db.commit()
            return res if res else 0
    except Exception as e:
        print(f"未知错误！=> {e}")
        return 0
    finally:
        print("insert_article() finally 释放链接")


# 更新文章的附件url
def update_file_url(title_id, file_paths):
    if file_paths is None:
        file_paths = ""  # 如果没有附件，设置为空字符串
    sql = """
            UPDATE article
            SET file_url = %s
            WHERE id = %s
            """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (file_paths, title_id))
            res = cursor.rowcount
            db.commit()
            return res if res else 0
    except Exception as e:
        print(f"未知错误！=> {e}")
        return 0
    finally:
        print("update_file_url() finally 释放链接")


# 查询文章内容
def search_fy_articles(keyword, page, limit):
    offset = (page - 1) * limit
    print(page, limit)
    sql = """
        SELECT id,title,username,date,contents,cover_url FROM article WHERE title LIKE %s LIMIT %s OFFSET %s;
    """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (f"%{keyword}%", limit, offset))
            results = cursor.fetchall()
            return results if results else []
    except Exception as e:
        print(f"未知错误！=> {e}")
        return []
    finally:
        print("search_articles() finally 释放链接")


# 搜索的数量
def select_search_count(keyword):
    sql = """
        SELECT count(*) as number FROM article WHERE title LIKE %s;
    """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (f"%{keyword}%"))
            results = cursor.fetchone()
            return results["number"] if results else 0
    except Exception as e:
        print(f"未知错误！=> {e}")
    finally:
        print("select_search_count() finally 释放链接")


# 获取所有文章类型
def getAllType():
    sql = "SELECT * FROM article_type;"
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            return results if results else []
    except Exception as e:
        print(f"未知错误！=> {e}")
        return []
    finally:
        print("getAllType() finally 释放链接")


# 文章的分页数据查询
def art_fy_data(article_page, limit, username):
    offset = (article_page - 1) * limit
    sql = """
        SELECT * FROM article AS c
        WHERE c.username = %s
        ORDER BY c.date DESC
        limit %s offset %s;
    """

    try:

        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (username, limit, offset))
            results = cursor.fetchall()
            return results if results else []
    except Exception as e:
        print(f"未知错误！=> {e}")
    finally:
        print("art_fy_data() finally 释放链接")


# 收藏的文章分页查询
def star_fy_data(starbook_page, limit, username):
    offset = (starbook_page - 1) * limit
    sql = """
        SELECT s.content_id,s.login_name,c.title,c.username FROM article as c 
        JOIN starbook as s 
        on s.content_id = c.id
        WHERE s.login_name = %s
        ORDER BY s.create_time DESC
        limit %s offset %s;
    """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (username, limit, offset))
            results = cursor.fetchall()
            return results if results else []
    except Exception as e:
        print(f"未知错误！=> {e}")
    finally:
        print("star_fy_data() finally 释放链接")


# 根据文章ID获取文章的总数
def select_all_content_by_typeid(typeid, limit, current_page):
    offset = (current_page - 1) * limit
    sql = """
            select c.*, a.nick_name, d.explain as `type_name`
            from article as c
                    RIGHT JOIN users as a
                                on c.username = a.username
                    RIGHT JOIN article_type as d
                                on d.id = c.typeid
            WHERE c.id is not null
            ORDER BY date DESC
            LIMIT %s OFFSET %s
    """
    if typeid != 0:
        sql = """
            select c.*, a.nick_name, d.explain as `type_name`
            from article as c
                    right join users as a
                                on c.username = a.username
                    right join article_type as d
                                on c.typeid = d.id
            where c.typeid = %s
            and c.id is not null
            ORDER BY date DESC
            LIMIT %s OFFSET %s;
        """
    try:

        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            if typeid == 0:
                cursor.execute(sql, (limit, offset))
            else:
                cursor.execute(sql, (typeid, limit, offset))
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"未知错误！=> {e}")
    finally:
        print("select_all_content_by_typeid() finally 释放链接")


# 主页查询最新的三条文章
def select_limit3_anyTypeInfo(typeid):
    sql = """
            	select c.*,a.nick_name,d.`explain` as `type_name` from article as c 
        RIGHT JOIN users as a
        on c.username = a.username
				RIGHT JOIN article_type as d
				on c.typeid = d.id
        WHERE c.id is not null and c.typeid = %s
        ORDER BY date DESC LIMIT 3
        """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, typeid)
            results = cursor.fetchall()
            return results if results else []
    except Exception as e:
        print(f"未知错误！=> {e}")
    finally:
        print("select_limit3_anyTypeInfo() finally 释放链接")


# 是否点赞
def isLikes(username, article_id):
    sql = """
        SELECT COUNT(*) AS number
        FROM tb_likes AS tb
            RIGHT JOIN users AS u ON tb.target_id = u.id
        WHERE
            u.username = %s
            AND tb.article_id = %s
    """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (username, article_id))
            result = cursor.fetchone()
            return result["number"] > 0 if result else False
    except Exception as e:
        print(f"未知错误！=> {e}")
        return False
    finally:
        print("isLikes() finally 释放链接")


# 添加点赞记录
def add_likes(title_id, username, user_id):
    sql = """
        INSERT INTO tb_likes (article_id, target_id, user_id)
        VALUES (%s, %s, %s)
    """
    target_id = getCurrentLoginId(username)
    if target_id is None:
        print("用户未登录或不存在")
        return False
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (title_id, target_id, user_id))
            db.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"未知错误！=> {e}")
        return False
    finally:
        print("add_likes() finally 释放链接")


# 取消点赞记录
def cancel_likes(title_id, username, user_id):
    sql = """
    DELETE FROM tb_likes WHERE user_id = %s AND target_id = %s AND article_id = %s
    """
    target_id = getCurrentLoginId(username)
    if target_id is None:
        print("用户未登录或不存在")
        return False
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (user_id, target_id, title_id))
            db.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"未知错误！=> {e}")
        return False
    finally:
        print("cancel_likes() finally 释放链接")


# 获取点赞数量
def getLikesNumber(title_id):
    sql = """
        SELECT likes_number FROM article WHERE id = %s
    """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (title_id,))
            result = cursor.fetchone()
            return result["likes_number"] if result else 0
    except Exception as e:
        print(f"未知错误！=> {e}")
        return 0
    finally:
        print("getLikesNumber() finally 释放链接")


# 获取当前登录用户的ID
def getCurrentLoginId(username):
    sql = """
        SELECT id FROM users WHERE username = %s
    """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            return result["id"] if result else None
    except Exception as e:
        print(f"未知错误！=> {e}")
        return None
    finally:
        print("getCurrentLoginId() finally 释放链接")


# 获取文章的封面
def getCoverByid(title_id):
    sql = """
        SELECT cover_url FROM article WHERE id = %s
    """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (title_id,))
            result = cursor.fetchone()
            return result["cover_url"] if result else {}
    except Exception as e:
        print(f"未知错误！=> {e}")
        return {}
    finally:
        print("getCoverByid() finally 释放链接")


def getContentTypeById(typeid):
    sql = """
        SELECT `explain` FROM article_type WHERE id = %s
    """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (typeid,))
            result = cursor.fetchone()
            return result["explain"] if result else "生活"
    except Exception as e:
        print(f"未知错误！=> {e}")
        return "生活"
    finally:
        print("getContentTypeById() finally 释放链接")
