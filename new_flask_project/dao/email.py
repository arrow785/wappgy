from sql_flask.mymysql import ConMySQL
from tools.mytools import get_time


def insert_emial(username,email,content,sqldb):
    connect, cursor = sqldb.mSQL()
    curr_time = get_time()
    sql = f"""
            insert into email(send_username,send_email,send_content,send_date,is_send) values (%s,%s,%s,%s,'失败')
        """
    try:
        cursor.execute(sql,(username,email,content,curr_time))
        connect.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f'insert_emial() 邮箱写入错误！！！ =>{e}')

def update_emial(username,sqldb):
    c,cour = sqldb.mSQL()
    sql = f"""update email set is_send = '成功' where send_username = %s"""
    try:
        cour.execute(sql,(username,))
        c.commit()
        return cour.rowcount
    except Exception as e:
        print(f'更新错误！！！ update_emial() => {e}')

def select_emial(username):
    con, cur = ConMySQL().mSQL()
    sql = f"""select * from email where send_username = %s"""
    try:
        cur.execute(sql,(username,))
        return cur.fetchall()
    except Exception as e:
        print(f'查询错误！！！ select_emial() => {e}')
    
    