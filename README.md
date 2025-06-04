# wappgy
个人开发
这是一个使用Python的Flask+Bootstrap5做的个人论坛

## 第一步

​	先安装环境..

```cmd
pip install requirements.txt -r
```



## 第二步

修改`sql_flask\MySQL_DB.py`中`ConMySQL`类的构造函数，将对应的`host`、`user`、`password`、`port`、`db_name`修改为本机的`mysql`地址、账户和密码

```python
# mysql的连接类

import pymysql
import pymysql.cursors

# 使用连接池
from dbutils.pooled_db import PooledDB


class ConMySQL:

    # 服务器 root@123
    def __init__(
        self,
        host="localhost",
        user="your_mysql_user",
        password="your_mysql_pwd",
        port=3306,
        db_name="your_db_name",
        pool_size=9,
    ):
        self.poool = PooledDB(
            creator=pymysql,
            maxconnections=pool_size, # 最大连接数
            mincached=2,  # 创建连接时，初始化连接数
            maxcached=3,
            blocking=True,  # 阻塞连接，当连接数达到最大时，后续连接请求会阻塞
            ping=0,  # 检测连接是否可用
            host=host,
            port=port,
            user=user,
            password=password,
            db=db_name,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def getConnect(self):
        try:
            return self.poool.connection()
        except Exception as e:
            print("数据库连接失败")
            raise e

```

## 第三步

去[DeepSeek官网](https://www.deepseek.com 'DeepSeek')`注册账号->API开放平台->充值->API Keys->创建API Key`，复制并保存key。打开`chat_config.py`文件修改，将你的key填入。

```python
class Ai_Config:
    DEEPSEEK_API_KEY = "your_deepseek_key"
    DEEPSEEK_API_URL = r"https://api.deepseek.com/v1/chat/completions"

```

## 第四步

修改主文件`app.py`文件中`/send_email`路由视图函数，**并且你需要去查询资料知道`Python Flask`项目如何发送`email`**

```python
@app.route("/send_email", methods=["POST"])
def send_email():
    data = request.form
    content = data.get("msg")
    name = session.get("username", "游客")
    email = ""
    username = session.get("username", "d")
    if username == "d" or username is None:
        email = "youke@youke@163.com"
    else:
        res = select_login_all(username)
        email = res["email"] if res else "youke@youke@163.com"

    # 配置 Flask-Mail
    app.config["MAIL_SERVER"] = "smtp.163.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = "your_email" # 发送者
    app.config["MAIL_PASSWORD"] = "yout_email_pwd"
    mail = Mail(app=app)
    msg = Message(
        subject=f"来自{name}的留言",
        sender="your_send_email", # 发送者
        recipients=["your_x_email_"], # 接受者
    )
    msg.body = f"来自{name}({email})的留言：{content}"
    try:
        row1 = insert_email(username=name, email=email, content=content)
        mail.send(msg)
        row2 = update_emial(username=name)
        if row1 and row2:
            return """
                    <script>
                        alert('发送成功！')
                        location.assign('/callme')
                    </script>"""
        else:
            return """
            <script>
                alert('发送成功！')
                location.assign('/callme')
            </script>"""
    except Exception as e:
        return f"""
            <script>
                alert('发送失败！服务器错误，请联系管理员！error=>{e}')
                location.assign('/callme')
            </script>
        """
    finally:
        print("发送邮件结束！")


```

待续.........有问题再补充
