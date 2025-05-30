from sql_flask.MySQL_DB import ConMySQL
from Tools import get_time

newConMysql = ConMySQL()


def insert_context(title, contents, username, type_id):
    current_time = get_time()
    sql = f"""
            insert into context(title,username,contents,date,typeid) values (%s,%s,%s,%s,%s)
        """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (title, username, contents, current_time, type_id))
            res = cursor.rowcount
            db.commit()
            return res if res > 0 else False
    except Exception as e:
        print(f"未知错误！=> {e}")
    finally:
        print("insert_context() finally 释放链接")


# def select_all_content_type(title_id: int):
#     connect, cursor = ConMySQL().mSQL()
#     sql = """
#         SELECT d.`explain` as `explain` FROM article_type as d
#         LEFT JOIN wz_leibie as w
#         on d.typeid = w.contentType
#         WHERE w.wz_id = %s;
#     """
#     with cursor:
#         cursor.execute(sql, title_id)
#         result = cursor.fetchall()
#         return result


def search_fy_contexts(keyword, page, limit):
    offset = (page - 1) * limit
    print(page, limit)
    sql = """
        SELECT id,title,username,date,contents FROM context WHERE title LIKE %s LIMIT %s OFFSET %s;
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
        print("search_contexts() finally 释放链接")


# 搜索的数量
def select_search_count(keyword):
    sql = """
        SELECT count(*) as number FROM context WHERE title LIKE %s;
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


def art_fy_data(article_page, limit, username):
    offset = (article_page - 1) * limit
    sql = """
        SELECT * FROM context AS c
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


def star_fy_data(starbook_page, limit, username):
    offset = (starbook_page - 1) * limit
    sql = """
        SELECT s.content_id,s.login_name,c.title,c.username FROM context as c 
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


def select_all_content_by_typeid(typeid, limit, current_page):
    offset = (current_page - 1) * limit
    sql = """
            select c.*, a.nick_name, d.explain as `type_name`
            from context as c
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
            from context as c
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


def select_limit3_anyTypeInfo(typeid):
    sql = """
            	select c.*,a.nick_name,d.`explain` as `type_name` from context as c 
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


# 获取类型文章的数量
# def get_articles_by_type_id_count(type_id):
#     sql ="""
#         SELECT
#         """
#     pass
