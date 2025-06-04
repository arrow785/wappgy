from sql_flask.MySQL_DB import ConMySQL

from dao.index import get_total_articles, select_all
import math

newConMysql = ConMySQL()


# 管理员登录


def admin_check_user(username, password):
    sql = """
        SELECT username,power from users where username = %s and pwd = %s;
    """
    try:
        with newConMysql.getConnect() as db:
            with db.cursor() as cur:
                cur.execute(sql, (username, password))
                result = cur.fetchone()
                return result if result else None
    except Exception as e:
        print("admin_check_user error: ", e)
        return None
    finally:
        print("admin_check_user finally")


# 管理员 LIMIT 查询
def admin_select_allArt(limit, page):
    offset = abs((page - 1)) * limit
    sql = """
        select * from article limit %s offset %s
    """
    try:
        with newConMysql.getConnect() as db:
            with db.cursor() as cur:
                cur.execute(sql, (limit, offset))
                result = cur.fetchall()
                return result if result else []
    except Exception as e:
        print("admin_select_allArt error: ", e)
        return []
    finally:
        print("admin_select_allArt finally")


# 管理员根据 id查询文章的内容
def admin_select_content_by_id(title_id):
    sql = """
        select * from article where id=%s
    """
    try:
        with newConMysql.getConnect() as db:
            with db.cursor() as cur:
                cur.execute(sql, (title_id,))
                result = cur.fetchone()
                return result if result else None
    except Exception as e:
        print("admin_select_content_by_id error: ", e)
        return None


def select_all_users(limit, offset):
    offset = (offset - 1) * limit
    sql = """
        select * from users where power = 0 limit %s offset %s
    """
    try:

        with newConMysql.getConnect() as db:
            with db.cursor() as cur:
                cur.execute(sql, (limit, offset))
                result = cur.fetchall()
                print(f"cur.lastrowid==>{cur.rownumber}")
                return result if result else None
    except Exception as e:
        print("select_all_users error: ", e)
        return None


def get_total_users():
    sql = """
        select count(*) as total from users where power != 1
    """
    try:
        with newConMysql.getConnect() as db:
            with db.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchone()
                return result["total"] if result else 0
    except Exception as e:
        print("get_total_users error: ", e)
        return None


def deleteUserById(username):
    sql = """
        DELETE from users where username = %s
    """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (username,))
        db.commit()
        # sql1 = """DELETE FROM article as c WHERE c.username = %s """
        # cur.execute(sql1, (username,))
        # db.commit()
        row = cur.rowcount
        return row > 0


def admin_users_(limit, page):
    offset = (page - 1) * limit
    sql = """
        select * from users where power != 1 limit %s offset %s
    """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (limit, offset))
        result = cur.fetchall()
        return result if result else None


def load_admin_paper_pages():
    datas = select_all(1, offset=3)
    total_perpers = get_total_articles()
    # 总页数
    total_pages = math.ceil(total_perpers / 3)
    print(f"load_admin_paper_pages {total_pages}")

    return {"datas": datas, "total_pages": total_pages}


def delete_article(id, title=""):
    sql = """
        delete from article where  id=%s
    """
    try:
        with newConMysql.getConnect() as db:
            with db.cursor() as cur:
                cur.execute(sql, (id,))
                db.commit()
                res = cur.rowcount
                return res if res else 0
    except Exception as e:
        print("delete_article error: ", e)
        return 0
    finally:
        print("delete_article finally")


def search_users(keyword):
    sql = f"""
                    select u.id,u.nick_name as nick_name,u.avatar,introduce as bio,u.username from users as u where nick_name like %s and u.power = 0;
                """

    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (f"%{keyword}%"))
        result = cur.fetchall()
        return result if result else []


# 管理员查看用户信息
def select_userinfo_By_id(userid):
    sql = """
        select * from users where id=%s
    """
    try:
        with newConMysql.getConnect() as db:
            cur = db.cursor()
            cur.execute(sql, (userid,))
            result = cur.fetchone()
            return result if result else {}
    except Exception as e:
        print("select_userinfo_By_id error: ", e)
    finally:
        print("select_userinfo_By_id finally")


def admin_update_user(uid, nickname, email, power):
    print(f"admin_update_user {uid},{nickname},{type(email)},{type(power)}")
    sql = """
        update users set nick_name=%s , email=%s , power=%s where id=%s
    """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (nickname, email, power, uid))
        db.commit()
        res = cur.rowcount
        return res if res else 0
