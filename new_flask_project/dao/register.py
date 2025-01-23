from sql_flask.mymysql import ConMySQL

connect, cursor = ConMySQL().mSQL()


def insert_user(username, email, password):
    try:
        if email is '':
            sql = f"""
                insert into admin (username,email,pwd) values (%s,null,%s)
            """
            cursor.execute(sql, (username, password))
        else:
            sql = f"""
                        insert into admin (username,email,pwd) values (%s,%s,%s)
                    """
            cursor.execute(sql, (username, email, password))
        connect.commit()
    except Exception as e:
        print(f'未知错误！=> {e}')
    return cursor.lastrowid
