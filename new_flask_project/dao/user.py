from sql_flask.mymysql import ConMySQL
from tools.mytools import get_time

connect, cursor = ConMySQL().mSQL()


# 用户注册
def insertUser(username, email, password, nickName, register_date):
    default_avatar = r"static\upload_img\mr.png"
    sql = f"""
                    insert into admin (username,nick_name,email,pwd,introduce,avatar,register_date) values (%s,%s,%s,%s,%s,%s,%s)
                """
    try:
        cursor.execute(sql, (username, nickName, email, password, '什么都没有！', default_avatar, register_date))
        connect.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f'insert_user() 写入用户失败 => {e}')


def check_user(username, password):
    sql = """
            SELECT COUNT(*) AS c FROM admin AS a WHERE a.username = %s AND a.pwd = %s;
        """
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()['c']
    print(result)
    return result


def check_(username):
    sql = """
            SELECT COUNT(*) AS c FROM admin AS a WHERE a.username = %s;
        """
    try:
        cursor.execute(sql, (username,))
        result = cursor.fetchone()['c']
        print(result)
        return result
    except Exception as e:
        print(f'check_() 错误！=> {e}')


# 登录时，检测账号密码是否正确
def d_login_check(username, password):
    sql = """
            SELECT COUNT(*) AS c FROM admin AS a WHERE a.username = %s AND a.pwd = %s;
        """
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()['c']
    print(result)
    return result


# 重置密码
def resetPwd(new_pwd, username):
    sql = """
            UPDATE admin SET pwd = %s WHERE username = %s;
        """
    cursor.execute(sql, (new_pwd, username))
    connect.commit()
    return cursor.rowcount


def selectAll(username, sqldb=ConMySQL()):
    con, cur = sqldb.mSQL()
    if username == 'd':
        return None
    sql = """
               SELECT * FROM admin AS a WHERE a.username = %s;
           """
    try:
        cur.execute(sql, (username,))
        result = cur.fetchone()
        print(f'selectAll() => {result}')
        return result
    except Exception as e:
        print(f'根据id查询文章内容 full_context() 错误！=> {e}')
        con.rollback()


# 更新密码
def updatePwd(username, pwd):
    sql = """
            UPDATE admin SET pwd = %s WHERE username = %s;
        """
    try:
        cursor.execute(sql, (pwd, username))
        connect.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f'updatePwd() 密码更新错误！！！ =>{e}')


# 获取旧密码
def getOldPwd(username):
    sql = """
            SELECT pwd FROM admin WHERE username = %s;
        """
    try:
        print(username)
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        print(result)
        return result.get('pwd')
    except Exception as e:
        print(f'获取旧密码错误 getOldPwd() 错误！=> {e}')
        connect.rollback()


# 更新资料
def update_user(username, email, nickName, introduce, avatar, sqldb):
    con, cur = sqldb.mSQL()
    sql = """
            UPDATE admin SET email = %s, nick_name = %s, introduce = %s, avatar = %s WHERE username = %s;
        """
    try:
        cur.execute(sql, (email, nickName, introduce, avatar, username))
        con.commit()
        print('update_user() => 更新成功！')
        return cur.lastrowid
    except Exception as e:
        print(f'update_user() 更新资料错误！！！ =>{e}')


def show_info(username: str):
    sql = """
            SELECT * FROM admin WHERE username = %s;
        """
    try:
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        print(f'show_info() => {result}')
        return result
    except Exception as e:
        print(f'show_info() 错误！=> {e}')
    finally:
        print('show_info() finally')


def selectGuestContext(sqldb=ConMySQL().mSQL()):
    sql = """
        SELECT * FROM guestbook AS gb ORDER BY gb.id DESC;
        """
    try:
        con, cur = sqldb.mSQL()
        cur.execute(sql)
        datas = cur.fetchall()
        print(f'selectGuestContext() => {datas}')
        return datas
    except Exception as e:
        print(f'selectGuestContext() 错误！=> {e}')
    finally:
        print('selectGuestContext() finally')


def insertGuestContext(username, context, avatar):
    date = get_time()
    avatar_path = ""
    if username == '游客':
        avatar_path = r"static\upload_img\yk.png"
    else:
        avatar_path = avatar
    sql = """
        INSERT INTO guestbook (username,context,date,avatar) VALUES (%s,%s,%s,%s);
        """
    try:
        cursor.execute(sql, (username, context, date, avatar_path))
        connect.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f'insertGuestContext() 错误！=> {e}')
    finally:
        print('insertGuestContext() finally')
