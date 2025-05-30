from sql_flask.MySQL_DB import ConMySQL
from Tools import get_time

newConMysql = ConMySQL()


# 用户注册
def insertUser(username, email, password, nickName, register_date):
    default_avatar = r"static\\upload_img\\bgc\\mr_bg1.png"
    sql = f"""
                    insert into users (username,nick_name,email,pwd,introduce,register_date) values (%s,%s,%s,%s,%s,%s)
                """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(
            sql,
            (
                username,
                nickName,
                email,
                password,
                "什么都没有！",
                register_date,
            ),
        )
        db.commit()
        res = cur.rowcount
        return res if res else 0


def check_user(username, password):
    sql = """
            SELECT a.id, a.power FROM users AS a WHERE a.username = %s AND a.pwd = %s;
        """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (username, password))
        result = cur.fetchone()
        return result if result else None


def check_(username):
    sql = """
            SELECT COUNT(*) AS c FROM users AS a WHERE a.username = %s;
        """

    with newConMysql.getConnect() as db:
        cursor = db.cursor()
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        return result["c"] if result else 0


# 登录时，检测账号密码是否正确
def d_login_check(username, password):
    sql = """
            SELECT COUNT(*) AS c FROM users AS a WHERE a.username = %s AND a.pwd = %s;
        """
    with newConMysql.getConnect() as db:
        cursor = db.cursor()
        cursor.execute(sql, (username, password))
        result = cursor.fetchone()
        return result["c"] if result else 0


# 重置密码
def resetPwd(new_pwd, username):
    if checkPwdIsExists(username, new_pwd):
        # 密码已存在
        return False
    else:
        sql = """
                UPDATE users SET pwd = %s WHERE username = %s;
            """
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (new_pwd, username))
            db.commit()
            res = cursor.rowcount
            return res if res else 0


def checkPwdIsExists(newpwd, username):
    sql = """
            SELECT COUNT(*) AS c FROM users AS a WHERE a.username = %s AND a.pwd = %s;
        """
    with newConMysql.getConnect() as db:
        cursor = db.cursor()
        cursor.execute(sql, (username, newpwd))
        result = cursor.fetchone()
        return result["c"] if result else None


def selectAll(username):
    if username == "d":
        return None
    sql = """
               SELECT * FROM users AS a WHERE a.username = %s;
           """

    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (username,))
        result = cur.fetchone()
        return result if result else {}


# 更新密码
def updatePwd(username, pwd):
    sql = """
            UPDATE users SET pwd = %s WHERE username = %s;
        """
    with newConMysql.getConnect() as db:
        cursor = db.cursor()
        cursor.execute(sql, (pwd, username))
        db.commit()
        res = cursor.rowcount
        return res if res else 0


# 获取旧密码
def getOldPwd(username):
    sql = """
            SELECT pwd FROM users WHERE username = %s;
        """
    with newConMysql.getConnect() as db:
        cursor = db.cursor()
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        return result if result else None


# 更新资料
def update_user(username, email, nickName, introduce, avatar, bgimg):
    sql = """
            UPDATE users SET email = %s, nick_name = %s, introduce = %s, avatar = %s, bg_img = %s WHERE username = %s;
        """

    with newConMysql.getConnect() as con:
        cur = con.cursor()
        cur.execute(sql, (email, nickName, introduce, avatar, bgimg, username))
        con.commit()
        res = cur.rowcount
        return res if res else 0


def show_info(username: str):
    sql = """
            SELECT * FROM users WHERE username = %s;
        """
    with newConMysql.getConnect() as db:
        cur = db.cursor()
        cur.execute(sql, (username,))
        result = cur.fetchone()
        return result if result else None


def selectGuestContext():
    sql = """
        SELECT * FROM guestbook AS gb ORDER BY gb.id DESC;
        """
    try:
        with newConMysql.getConnect() as db:
            cur = db.cursor()
            cur.execute(sql)
            datas = cur.fetchall()
            return datas if datas else []
    except Exception as e:
        print(f"selectGuestContext() 错误！=> {e}")
    finally:
        print("selectGuestContext() finally")


def insertGuestContext(username, context, avatar):
    date = get_time()
    avatar_path = ""
    if username == "游客":
        avatar_path = r"static\upload_img\yk.png"
    else:
        avatar_path = avatar
    sql = """
        INSERT INTO guestbook (username,context,date,avatar) VALUES (%s,%s,%s,%s);
        """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (username, context, date, avatar_path))
            db.commit()
            res = cursor.rowcount
        return res if res else 0
    except Exception as e:
        print(f"insertGuestContext() 错误！=> {e}")
    finally:
        print("insertGuestContext() finally")


def select_star_books(loginname):
    sql = """
    SELECT s.content_id,s.login_name,c.title,c.username FROM context as c 
        JOIN starbook as s 
        on s.content_id = c.id
        WHERE s.login_name = %s
    """
    try:
        with newConMysql.getConnect() as db:
            cursor = db.cursor()
            cursor.execute(sql, (loginname,))
            data = cursor.fetchall()
            # print(f"select_star_books() => {data}")
            return data if data else []
    except Exception as e:
        print(f"select_star_books() 错误！=> {e}")
        return []
    finally:
        print("select_star_books() 释放连接")
