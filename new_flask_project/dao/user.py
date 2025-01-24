from sql_flask.mymysql import ConMySQL
from tools.mytools import md5

connect, cursor = ConMySQL().mSQL()


# 用户注册
def insertUser(username, email, password, avatar, nickName, register_date):
    sql = f"""
                    insert into admin (username,nick_name,email,pwd,introduce,avatar,register_date) values (%s,%s,%s,%s,%s,%s,%s)
                """
    try:
        cursor.execute(sql, (username, nickName, email, password, '什么都没有！', avatar, register_date))
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
    cursor.execute(sql, (username, md5(password)))
    result = cursor.fetchone()['c']
    print(result)
    return result


# 重置密码
def resetPwd(new_pwd, username):
    sql = """
            UPDATE admin SET pwd = %s WHERE username = %s;
        """
    cursor.execute(sql, (md5(new_pwd), username))
    connect.commit()
    return cursor.rowcount


def selectAll(username,sqldb):
    con,cur = sqldb.mSQL()
    if username == 'd':
        return None
    sql = """
               SELECT * FROM admin AS a WHERE a.username = %s;
           """
    try:
        cur.execute(sql, (username,))
        result = cur.fetchone()
        print(result)
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
def update_user(username, email, nickName, introduce, avatar):
    sql = """
            UPDATE admin SET email = %s, nick_name = %s, introduce = %s, avatar = %s WHERE username = %s;
        """
    try:
        cursor.execute(sql, (email, nickName, introduce, avatar, username))
        connect.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f'update_user() 更新资料错误！！！ =>{e}')
