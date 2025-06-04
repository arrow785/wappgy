from sql_flask.MySQL_DB import ConMySQL
from Tools import get_time

newConMysql = ConMySQL()


def getHistory(user_id, used):
    sql = "select role,content from chat_history where user_id = %s and used = %s"
    try:
        with newConMysql.getConnect() as db:
            with db.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        user_id,
                        used,
                    ),
                )
                result = cur.fetchall()
                return result if result else []
    except Exception as e:
        print(f"getHistory() 获取历史记录错误！=> {e}")
        return []
    finally:
        print("getHistory() finally")


def insert_msg(user_id, role, content, model, used):
    sql = """
    INSERT INTO chat_history(user_id,role,content,model,used)
    VALUES(%s,%s,%s,%s,%s);
    """
    try:
        with newConMysql.getConnect() as db:
            with db.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        user_id,
                        role,
                        content,
                        model,
                        used,
                    ),
                )
                db.commit()
                res = cur.rowcount
                return res > 0
    except Exception as e:
        print(f"insert_msg() 插入历史记录错误！=> {e}")
        return False
    finally:
        print("insert_msg() finally")
