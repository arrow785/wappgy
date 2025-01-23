from sql_flask.mymysql import ConMySQL
from tools.mytools import md5
connect,cursor = ConMySQL().mSQL()

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
    cursor.execute(sql, (username))
    result = cursor.fetchone()['c']
    print(result)
    return result

def resetPwd(new_pwd, username):
    sql = """
            UPDATE admin SET pwd = %s WHERE username = %s;
        """
    cursor.execute(sql, (md5(new_pwd), username))
    connect.commit()
    return cursor.rowcount
    