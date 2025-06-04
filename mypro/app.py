# 主程序

from functools import wraps
from flask import (
    render_template,
    request,
    session,
    redirect,
    url_for,
    jsonify,
    send_from_directory,
    Response,
)
from flask_cors import CORS
import requests
import math
from dao.Starbook import *
from sql_flask.Flask_Settings import MyFlask as _Flask
from flask_mail import Mail, Message
from dao.index import *
from dao.Users import *
from dao.manager import *
from dao.Article import *
from dao.Detailed import *
from dao.Email import *
from dao.Admin import *
from dao.Chat import *
from config import Config
from Tools import *
import json


def split_filter_jinja2(value, sub=None):
    if sub is None:
        return value
    # 默认使用逗号分割
    return value.split(sub)


flask = _Flask(app_name=__name__, port=5002, host="localhost", debug=True)

app = flask.app
app.config.from_object(Config)
app.jinja_env.filters["split"] = split_filter_jinja2
CORS(app)


# 允许的图片格式
def allowed_file_img(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "png",
        "jpg",
        "jpeg",
    }


# 允许的文件格式
def allowed_file_zip(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "zip",
        "rar",
        "tar",
        "gz",
        "7z",
        "pdf",
        "docx",
        "txt",
        "xlsx",
        "pptx",
        "doc",
        "xls",
        "ini",
        "sql",
        "py",
        "java",
        "c",
        "cpp",
        "cs",
    }


information: dict = {}
loginUser: dict = {}


# 登录装饰器
def my_login_required(func):

    @wraps(func)  # 使用装饰器wraps来保留被装饰函数的元数据
    def wrapper(*args, **kwargs):
        # 打印调试信息，检查会话状态
        print("Checking session:", session)  # 添加调试信息
        if session.get("username", "d") == "d":
            # 如果会话中没有用户名或用户名不是"d"，则视为用户未登录
            print("User not logged in, redirecting to main view")
            return redirect(url_for("login"))
        else:
            # 如果用户已登录，则执行原函数
            print("User logged in, proceeding")
            return func(*args, **kwargs)

    return wrapper


# 设置密钥
def get_salt():
    import string, random

    salt: str = "".join(random.sample(string.ascii_letters + string.digits, 8))
    return salt


app.config["SECRET_KEY"] = get_salt()
# string随机盐生成


# 更新字典information的数据
def update_information(username):
    information["data"] = select_login_all(username)


def set_session(username, power):
    session["username"] = username
    session["power"] = power
    if username is None:
        session["username"] = "d"

    else:
        update_information(username)
        print(information.get("data"))


# ----------------------------- 首页路由 ---------------------------------------------------
# ----------------------------- 首页路由 ---------------------------------------------------
@app.route("/", methods=["GET"])
def main():
    return redirect(url_for("index"), code=302)


@app.route("/index", methods=["GET"])
def index():
    # 获取最新文章
    current_page = request.args.get("page", 1, type=int)  # 更改变量名为current_page
    # limit
    limit = 8
    # 获取当前的类型ID
    typeid = request.args.get("typeid", 0, type=int)
    # 获取文章总数
    total_articles = get_total_articles(typeid=typeid)
    total_pages = totalPage(total_articles, limit)

    username = session.get("username", "d")
    avatar_path = get_avatar(username=username)
    nick_name = getNickName(session.get("username", "d"))
    allTypes = getAllType()
    # 各类别最新文章 limit = 3
    all_ = {"all_data": []}
    for i in allTypes:
        _articles = select_limit3_anyTypeInfo(i.get("typeid"))
        all_["all_data"].append(
            {
                "typeid": i.get("typeid"),
                "type_name": i.get("explain"),
                "infos": _articles,
            }
        )
    cover_url = getCoverByid(typeid)
    print(f"cover_url==>{cover_url}")
    datas = select_all_content_by_typeid(typeid, limit, current_page)
    return render_template(
        "index.html",
        current_page=current_page,
        total_pages=total_pages,
        datas=datas,
        nickname=nick_name,
        avatar_path=avatar_path,
        types=allTypes,
        typeid=typeid,
        all_data=all_,
    )


# --------------------------------------------- 文章相关路由 ---------------------------------------------------
# --------------------------------------------- 文章相关路由 ---------------------------------------------------


@app.route("/write", methods=["GET", "POST"])
@my_login_required
def write():
    if request.method == "GET":
        username = session.get("username", "d")
        avatar_path = information.get("data", {}).get("avatar")
        allTypes = getAllType()
        power = session.get("power", -1)
        nick_name = getNickName(username=username)
        if power == 2:
            return """
            <script>
                alert('您已经被禁止发布文章，更多信息请联系管理员！')
                location.assign('/index')
            </script>
        """
        elif power == 1:
            return """
            <script>
                alert('您没有登录！')
                location.assign('/index')
            </script>
        """
        return render_template("write.html", **locals())
    elif request.method == "POST":
        data = request.form
        cover_img = request.files.get("cover_img")
        # 获取上传的文件
        files = request.files.getlist("zipfiles")
        if files[0].filename != "":
            for x in files:
                if not allowed_file_zip(x.filename):
                    return """
                    <script>
                        alert('不支持的文件类型！请上传zip格式的文件。')
                        window.history.back();
                    </script>
                """
        if cover_img:
            if cover_img and not allowed_file_img(cover_img.filename):
                return """
                    <script>
                        alert('不支持的文件类型！请上传jpg、jpeg或png格式的图片。')
                        window.history.back();
                    </script>
                """

        print(f"cover_img==>{cover_img}")
        typeid = data.get("content_type")
        title = data.get("title")
        context = data.get("content")
        cover_path = ""

        cover_path = save_cover_to_system(
            imgfile=cover_img,
            lid=information.get("data", {}).get("id"),
        )
        res = insert_article(
            title,
            context,
            session.get("username"),
            type_id=typeid,
            cover_path=cover_path,
        )
        paths = save_attachment(files=files, title_id=res)
        row = update_file_url(title_id=res, file_paths=paths)
        if res == 0 or row == 0:
            return """ <script>
                    alert('添加文章失败！');
                    window.history.back();
                   
        </script>"""

        return redirect(url_for("index", page=1))
    else:
        return """
            <script>
                alert('不支持的请求方式')
               window.history.back();
            </script>
            """


# 获取文章详情
@app.route("/detalied/<int:title_id>", methods=["GET"])
def detalied(title_id: int):
    data = full_article(title_id)
    article_id = data.get("id")
    if len(data) == 0:
        return render_template("404.html", msg="啊欧，这个文章不小心走丢了！")
    #
    username = session.get("username", "d")
    avatar_path = information.get("data", {}).get("avatar")
    is_star_book = isStarBook(username, article_id)
    print(f"is_star_book() => {is_star_book}")
    is_likes = isLikes(username, article_id)
    # filePathx = data.get("file_url", "").split(",")
    # 获取当前登录用户的最新三条数据
    latest_article = getLatestArticleByUsername(data.get("username"))
    # 获取收藏总数
    star_number = getStarNumber(title_id=title_id)
    # detailed
    return render_template("detailed.html", **locals())


# 获取评论数
@app.route("/api/<int:title_id>/get_comments")
def get_comments(title_id: int):
    limit = 3
    comments_count = by_id_get_comments(title_id)
    page = request.args.get("page", 1, type=int)
    total_pages = totalPage(comments_count, limit)
    fy_data = by_id_get_comments_fy_data(page=page, limit=limit, titleid=title_id)
    if fy_data:
        return jsonify(
            {
                "code": 200,
                "msg": "success",
                "comments": fy_data,
                "total_pages": total_pages,
                "current_page": page,
            }
        )
    else:
        return jsonify(
            {
                "code": 500,
                "msg": "fail",
                "comments": {},
                "total_pages": 0,
                "current_page": 0,
            }
        )


# 提交评论路由
@app.route("/comment_submit", methods=["POST"])
def comment_submit():
    data = request.args
    title_id = data.get("title_id", 0, type=int)
    username = data.get("username", "", type=str)
    zhuti = data.get("zhuti", "", type=str)
    if title_id == 0 or username == "" or zhuti == "":
        return jsonify({"code": 0, "msg": "参数错误，请重试！"})
    comments = request.get_json().get("comment")
    if comments == "":
        return jsonify({"code": 0, "msg": "评论内容不能为空！"})

    res = insert_comment(username, comments, title_id, zhuti=zhuti)

    if res:
        return jsonify({"code": 1, "msg": "评论成功！"})
    else:
        return jsonify({"code": 0, "msg": "评论失败，请联系管理员！"})


# 点赞路由
@app.route("/likes", methods=["GET"])
def likes():

    title_id = request.args.get("id")
    type_ = request.args.get("type")
    user_id = request.args.get("user_id", type=int)
    username = session.get("username", "d")
    if type_ == "like":
        row = add_likes(title_id, username, user_id)
    elif type_ == "unlike":
        row = cancel_likes(title_id, username, user_id)
    else:
        return jsonify({"status": "error", "message": "不合法的类型"})
    likesNumber = getLikesNumber(title_id=title_id)
    return jsonify({"status": row, "likesNumber": likesNumber})


# ---------------------------------------------------用户相关路由--------------------------------------------------------
# ---------------------------------------------------用户相关路由--------------------------------------------------------
# 登录
@app.route("/login", methods=["GET", "POST"])
def login():
    username = session.get("username", "d")
    if username != "d":
        return """
            <script>
                alert('您已经登录！请勿重复登录！')
                location.assign('/index')
            </script>
            """
    if request.method == "POST":
        data = request.form
        username = data.get("username", "")
        email = ""
        if "@" in username:
            email = username
        password = data.get("password")
        rows = check_user(username, email, password)
        print(f"login() => {rows}")
        if rows is None:
            return """
                    <script>
                            alert('用户或邮箱、密码错误！')
                            location.assign('/login')
                    </script>
                    """
        elif rows:
            set_session(rows.get("username"), power=rows["power"])
            if rows["power"] != 1 and rows["power"] != 3:
                return """
                            <script>
                                location.assign('/index')
                            </script>
                        """
            elif rows["power"] == 1:
                return """
                    <script>
                        alert('账号不允许使用该接口登录。')
                        window.location.assign('/login')
                    </script>
                
                    """
            elif rows["power"] == 3:
                return """
                    <script>
                        alert('被封禁的账户，请联系管理员。')
                        window.location.assign('/login')
                    </script>
                
                    """
            else:
                return """
                        <script>
                                alert('未知错误，请联系管理员！')
                        </script>
                        """
        else:
            return """
                <script>
                        alert('未知错误！！！')
                        location.assign('/login')
                </script>
                """
    elif request.method == "GET":

        if username != "d":
            return """
                <script>
                    alert('您已经登录！')
                    location.assign('/index')
                </script>
                """
        return render_template("login.html")
    else:
        return """
            <script>
                alert('不允许的请求方法！！！')
                location.assign('/login')
            </script>
            """


# 注册路由
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        # 获取当前时间
        register_date = get_time()

        nickName = data.get("nickname")
        # 如果用户没有填昵称则获取随机昵称
        if nickName == "":
            nickName = randName()
        password = data.get("password")
        pwd_test = data.get("password-test")
        # 再次判断密码是否一致
        if password != pwd_test:
            return jsonify({"code": 0, "msg": "两次密码不一致!"})
        email = data.get("email")

        rows = insertUser(
            username=username,
            email=email,
            password=password,
            register_date=register_date,
            nickName=nickName,
        )
        if rows is not None:
            return jsonify({"code": 1, "msg": "注册成功!"})
        else:
            return jsonify({"code": 2, "msg": "注册失败!"})
    return render_template("register.html")


# 重置密码路由
@app.route("/reset_pwd", methods=["GET", "POST"])
def reset_pwd():
    if request.method == "GET":
        return render_template("resetpwd.html")
    elif request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        print(f"reset_pwd1() => : username==>{username},password==>{password}")
        row = resetPwd(new_pwd=password, username=username)
        if row == False:
            return jsonify({"code": 0, "msg": "新密码不能与旧密码相同！"})
        if row is not None:
            return jsonify({"code": 1, "msg": "修改成功！"})
        else:
            return jsonify({"code": 2, "msg": "修改失败！"})
    else:
        return """
        <script>
        alert("不支持的请求 方法！");
        </script>

        """


# ------------------------------------------- 退出登录路由 ---------------------------------------------------
# ------------------------------------------- 退出登录路由 ---------------------------------------------------
@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("main"))


# ------------------------------------------- 其他异步路由 ---------------------------------------------------
# ------------------------------------------- 其他异步路由 ---------------------------------------------------
# 注册时，判断用户名是否已经存在
@app.route("/check_username/<string:username>", methods=["GET"])
def check_username(username: str):
    rows = check_(username=username)
    print(f"check_username=>{username}")
    if len(rows) == 0:
        return jsonify({"exists": False, "msg": "用户名不存在"})
    else:
        return jsonify({"exists": True, "msg": "--"})


#  检查旧密码 用于异步请求
@app.route("/checkoldpwd", methods=["POST"])
def checkoldpwd():
    oldPwd = getOldPwd(session.get("username", "d"))
    newpwd = request.get_json().get("pwd1")
    print(oldPwd, newpwd)
    if oldPwd == newpwd:
        return jsonify(exists=True)
    return jsonify(exists=False)


# ------------------------ 开发者相关路由 ---------------------------------------------------
# ------------------------ 开发者相关路由 ---------------------------------------------------
@app.route("/pep_dev", methods=["GET"])
def pep():
    datas = select_article_by_username(username="喜欢劈瓜的刘华强")
    print(datas)
    if datas is not None:
        return render_template("dev_people.html", **locals())
    else:
        datas = {}
        return render_template("dev_people.html", **locals())


# ----------------------------------留言、联系、发送邮箱---------------------------------------------------------------------
# ----------------------------------留言、联系、发送邮箱---------------------------------------------------------------------
# 留言板路由
@app.route("/boards", methods=["GET"])
def boards():
    # 获取留言板的数据
    datas = selectGuestContext()
    return render_template("guestbook.html", **locals())


# 联系我
@app.route("/callme", methods=["GET"])
def callme():
    return render_template("callme.html")


# 发送邮件
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
    app.config["MAIL_USERNAME"] = "xttdfix@163.com"
    app.config["MAIL_PASSWORD"] = "LVgPZrqcMmmWFUdq"
    mail = Mail(app=app)
    msg = Message(
        subject=f"来自{name}的留言",
        sender="xttdfix@163.com",
        recipients=["luoruiGeng@163.com"],
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


@app.route("/guestbook", methods=["POST"])
def guestbook():
    username = session.get("username", "游客")
    print(f"guestbook() => {username}")
    avatar_path = get_avatar(username=username)
    row = insertGuestContext(
        username=username, context=request.form.get("context"), avatar=avatar_path
    )
    if row is not None:
        return redirect(url_for("boards"))
    else:
        return """
                <script>
                    alert('留言失败！未知错误，请联系开发者')
                    location.assign('/boards')
                </script>
               """


#  ----------------------------------------------------- 个人中心 -----------------------------------------------------------
#  ------------------------------------------------------- 个人中心 ------------------------------------------------------------
@app.route("/people", methods=["GET"])
@my_login_required
def people():
    username = session.get("username", "d")
    ifm = information.get("data", {})
    print(f"ifm ==> {ifm}")
    contexts = select_article_by_username(username=username)
    emails = select_emial_count(login_username=username)
    # 获取收藏文章
    stars = select_star_books_count(login_username=username)

    # 以下的数据都是分页数据
    limit = 5
    # 文章page
    article_page = request.args.get("article_page", 1, type=int)
    art_pages = totalPage(total_count=stars, limit=limit)
    article_fy_data = art_fy_data(
        article_page=article_page, limit=limit, username=username
    )
    # 收藏
    starbook_page = request.args.get("starbook_page", 1, type=int)
    star_pages = totalPage(total_count=stars, limit=limit)
    st_fy_data = star_fy_data(
        starbook_page=starbook_page, limit=limit, username=username
    )

    # 邮箱
    email_page = request.args.get("email_page", 1, type=int)
    email_pages = totalPage(total_count=emails, limit=limit)
    em_fy_data = em_dy_data_(email_page=email_page, limit=limit, username=username)

    return render_template("people.html", **locals())


# 个人文章管理
@app.route("/manager", methods=["GET"])
@my_login_required
def manager():
    username = session.get("username")
    datas = select_article_by_username(username)
    avatar_path = information.get("data", {}).get("avatar")
    return render_template("manager.html", **locals())


# 个人文章编辑
@app.route("/edit", methods=["GET", "POST"])
@my_login_required
def edit():
    if request.method == "GET":
        title_id = request.args.get("title_id", 0, type=int)
        datas = find_article(title_id=title_id)
        avatar_path = get_avatar(session.get("username", "d"))
        allTypes = getAllType()
        return render_template("edit.html", **locals())
    elif request.method == "POST":
        datas = request.form
        title = datas.get("title")
        type_id = datas.get("content_type")
        content = datas.get("content")
        title_id = int(datas.get("title_id", 0))

        rows = update_content(
            title_id=title_id, content=content, title=title, type_id=type_id
        )
        if rows is not None:
            return """
                    <script>
                        alert('修改成功！')
                        location.assign('/manager')
                    </script>
                    """
        else:
            return """
                    <script>
                        alert('修改失败！')
                        location.assign('/manager')
                    </script>
                    """
    else:
        return """
                <script>
                    alert('不支持的请求方式')
                    location.assign('/manager')
                </script>
                """


#  删除文章路由
@app.route("/delete/<int:t_id>", methods=["GET"])
def delete(t_id: int):
    rows = delete_article(t_id)
    return jsonify(flg=rows > 0)


# 修改个人信息
@app.route("/update_info", methods=["POST"])
def update_info():
    """
    处理用户个人信息更新请求

    功能：
        - 接收并处理用户提交的表单数据
        - 保存用户上传的头像和背景图片
        - 更新用户昵称、邮箱、简介等基本信息
        - 根据操作结果返回重定向或错误提示

    返回值：
        redirect: 操作成功时重定向到用户主页
        str: 包含错误提示脚本的字符串（操作失败时返回）
    """
    data = request.form
    imgfile = data.get("croppedImage")
    name = session.get("username", "d")
    bgc_img = request.files["bgc_img"]

    avatar_path = save_avatar_to_system(
        imgfile=imgfile, lid=information.get("data", {}).get("id")
    )
    bgc_path = save_bgc_to_system(
        imgfile=bgc_img, lid=information.get("data", {}).get("id")
    )

    newnick = data.get("newnick")
    newemail = data.get("newemail")
    introduce = data.get("introduce")

    rows = update_user(
        username=session.get("username", "d"),
        email=newemail,
        nickName=newnick,
        introduce=introduce,
        avatar=avatar_path,
        bgimg=bgc_path,
    )
    update_information(name)
    if rows is not None:
        return redirect(url_for("people"))
    else:
        return """
                <script>
                    alert('修改失败！未知错误，请联系开发者')
                    location.assign('/people')
                </script>
               """


# 修改密码
@app.route("/update_pwd", methods=["post"])
def update_pwd():
    pwd = request.form.get("pwd")
    username = session.get("username", "d")

    # 判断和旧密码是否一致
    oldPwd = getOldPwd(username)
    rows = updatePwd(username=username, pwd=pwd)
    print(oldPwd)
    if oldPwd == pwd:
        return """
                <script>
                    alert('修改失败！新密码与旧密码一致，重新修改密码')
                    location.assign('/people')
                </script>
               """
    if rows is not None:
        return """
                <script>
                    alert('修改成功！请重新登陆！')
                    location.assign('/login')
                </script>
               """
    else:
        return """
                <script>
                    alert('修改失败！未知错误，请联系开发者')
                    location.assign('/people')
                </script>
               """


# 显示用户信息
@app.route("/show_information/<string:username>", methods=["GET"])
def show_information(username: str):
    data = show_info(username)
    contexts = select_article_by_username(username=username)
    username1 = session.get("username", "d")
    bgc_img = get_bgc(username=username)
    return render_template("user_people.html", **locals())


# -------------------------------------------- 版本信息 ---------------------------------------------------
# -------------------------------------------- 版本信息 ---------------------------------------------------
@app.route("/show_version", methods=["GET"])
def show_version():
    return render_template("version.html")


# 收藏
@app.route("/starbook", methods=["GET"])
def starbook():
    title_id = request.args.get("id")
    type_ = request.args.get("type")
    username = session.get("username", "d")
    if type_ == "star":
        row = star_book(title_id, username)
    elif type_ == "unstar":
        row = cancel_star_book(title_id, username)
    else:
        return jsonify({"status": "error", "message": "不合法的类型"})
    starNumber = getStarNumber(title_id=title_id)
    return jsonify({"status": row, "starNumber": starNumber})


# -------------------------------------------- 管理员相关路由 ---------------------------------------------------
# -------------------------------------------- 管理员相关路由 ---------------------------------------------------


# 管理员登录
@app.route("/admin_login", methods=["POST", "GET"])
def admin_login():
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")
        print(f"admin_login() => username: {username}, password: {password}")
        rows = admin_check_user(username, password)
        if rows is None:
            return """
                    <script>
                            alert('账户或者密码错误！')
                            location.assign('/admin_login')
                    </script>
                    """
        else:
            if rows["power"] == 1:
                return """
                    <script>
                            location.assign('/admin')
                    </script>
                    """
            else:
                return """
                    <script>
                            alert('您没有权限！')
                            location.assign('/admin_login')
                    </script>
                    """
    elif request.method == "GET":
        return render_template("admin_login.html")
    else:
        return """
                <script>
                        alert('不允许的请求！')
                        location.assign('/admin_login')
                </script>
                """


# 管理员编辑文章
@app.route("/admin/modify_content", methods=["GET", "POST"])
def admin_edit():
    if request.method == "POST":
        data = request.get_json()
        title_id = data.get("title_id")
        title = data.get("title")
        typeid = data.get("content_type")
        content = data.get("content")
        res = update_content(
            type_id=typeid, content=content, title=title, title_id=title_id
        )
        if res != 0:
            return jsonify({"code": 1, "msg": "更新成功"})
        return jsonify({"code": 0, "msg": "更新失败"})

    datas = admin_select_content_by_id(
        title_id=request.args.get("id"),
    )
    allTypes = getAllType()
    return render_template("admin_modify_content.html", **locals())


# 管理员页面
@app.route("/admin", methods=["GET"])
def admin():
    # 用户分页数据
    limit = 3
    user_current_page = request.args.get("user_current_page", 1, type=int)
    userCount = get_total_users()
    userPages = totalPage(userCount, limit)
    user_admin_fy_data = admin_users_(limit, user_current_page)

    # 文章分页数据
    article_current_page = request.args.get("article_current_page", 1, type=int)
    articleCount = get_total_articles()
    articlePages = totalPage(articleCount, limit)
    article_admin_fy_data = admin_select_allArt(limit, article_current_page)
    return render_template(
        "admin.html",
        user_current_page=user_current_page,
        user_Pages=userPages,
        userCount=userCount,
        user_admin_fy_data=user_admin_fy_data,
        article_current_page=article_current_page,
        article_Pages=articlePages,
        articleCount=articleCount,
        article_admin_fy_data=article_admin_fy_data,
    )


# 管理员修改用户信息
@app.route("/admin_modify_user", methods=["POST", "GET"])
def admin_modify_user():
    if request.method == "POST":
        data = request.get_json()
        nickname = data.get("nick_name")
        email = data.get("email")
        power = int(data.get("role"))
        uid = int(data.get("uid"))
        res = admin_update_user(uid=uid, nickname=nickname, email=email, power=power)
        if res:
            return jsonify({"code": 1, "msg": "更新成功"})
        else:
            return jsonify({"code": 0, "msg": "更新失败"})
    else:
        userid = request.args.get("id")
        print(f"admin_modify_user() => {userid}")
        user = select_userinfo_By_id(userid)
        return render_template("admin_modify_user.html", user=user)


@app.route("/admin/users", methods=["GET"])
def admin_users():
    page = request.args.get("page", 1, type=int)
    per_page = 3
    print(f"admin_users() => {page} {per_page}")
    users = select_all_users(per_page, page)
    total_perpers = get_total_users()
    total_pages = totalPage(total_perpers, per_page)
    return jsonify(
        {"users": users, "total_pages": total_pages, "current_user_page": page}
    )


# 管理员管理文章
@app.route("/admin/articles", methods=["GET"])
def admin_articles():
    page = request.args.get("page", 1, type=int)
    per_page = 3
    datas = select_all(
        per_page,
        page,
    )
    get_perpers = get_total_articles()

    # 总页数
    total_pages = math.ceil(get_perpers / per_page)

    return jsonify(
        {"data": datas, "total_pages": total_pages, "current_paper_page": page}
    )


@app.route("/admin/delete_article", methods=["GET"])
def admin_delete_article():
    id = request.args.get("id")
    if delete_article(id=id):
        return jsonify({"status": 200})
    return jsonify({"status": 400})


@app.route("/admin/deleteUserById", methods=["POST"])
def admin_deleteUserById():
    username = request.get_json().get("username")
    userid = request.get_json().get("id")
    if deleteUserById(username=username):
        return jsonify({"status": 200})
    return jsonify({"status": 400})


# -------------------------------------------- 搜索路由 ---------------------------------------------------
# -------------------------------------------- 搜索路由 ---------------------------------------------------
@app.route("/api/search", methods=["GET"])
def search_fy_api():
    limit = 4
    page = request.args.get("page", 1, type=int)
    keyword = request.args.get("keyword", "", type=str)
    searchCount = select_search_count(keyword)
    search_total_pages = totalPage(total_count=searchCount, limit=limit)
    search_fy_data = search_fy_articles(keyword=keyword, limit=limit, page=page)
    if search_fy_data:
        return jsonify(
            {
                "data": search_fy_data,
                "total_pages": search_total_pages,
                "current_page": page,
            }
        )
    else:
        return jsonify({"data": [], "total_pages": 0, "current_page": 0})


# 搜索
@app.route("/search", methods=["GET"])
def search():
    return render_template("search.html")


# -------------------------------------------- 标签相关路由 ---------------------------------------------------
# -------------------------------------------- 标签相关路由 ---------------------------------------------------
# 跳转到tag
@app.route("/tag")
def tag():
    tag = request.args.get("type_id", 0, type=int)
    if tag == 0:
        return """
            <script>
                alert("标签不存在")
                window.location.href = "/"
            </script>
            """
    type_name = getTypeName(tag)
    by_id_articleCount = get_total_articles(tag)
    username = session.get("username", "d")
    return render_template(
        "tag.html",
        tag=tag,
        by_id_articleCount=by_id_articleCount,
        username=username,
        avatar_path=get_avatar(username=username),
        type_name=type_name,
    )


# 获取标签下的文章，含分页功能
@app.route("/tag/<int:type_id>/articles")
def tag_articles_by_type_id(type_id):
    page = request.args.get("page", 1, type=int)
    by_type_id_count = get_total_articles(type_id)
    limit = 8
    by_type_id_allPages = totalPage(by_type_id_count, limit)
    by_type_id_fy_data = select_all_content_by_typeid(
        typeid=type_id, limit=limit, current_page=page
    )
    if by_type_id_fy_data:
        return jsonify(
            {
                "data": by_type_id_fy_data,
                "total_pages": by_type_id_allPages,
                "current_page": page,
            }
        )
    else:
        return jsonify({"data": [], "total_pages": 0, "current_page": 0})


@app.route("/tag/articles", methods=["GET"])
def tag_articles():
    tag = request.args.get("tag")

    return jsonify({"data": 1})


# ---------------------------------------- 人工智能相关路由 ---------------------------------------------------
# ---------------------------------------- 人工智能相关路由 ---------------------------------------------------


@app.route("/todeepseek", methods=["GET"])
def todeepseek():
    if session.get("username", "d") == "d":
        return """
    <script>
    alert("请先登录")
    window.location.href = "/login"
    </script>
"""
    return render_template("ds-index.html")


import datetime as dt

# 定义全局变量，记录对话记录
v3_history_ask = []
r1_history_ask = []


# V3 模型
def V3_model(
    used,
    question="",
    SYSTEM_INIT="你是一个通用AI助手(V3模型)，提供快速响应",
):

    client = OpenAI(
        api_key="sk-709b1426f00d42c880e1db9b43b22a3c",
        base_url="https://api.deepseek.com",
    )
    # 从数据库中获取历史记录
    user_id = information.get("data", {}).get("id")
    history = getHistory(user_id=user_id, used=used)
    msg = []
    if not history or SYSTEM_INIT != "你是一个有趣的AI助手，擅长日常问题的回答":
        msg.append({"role": "system", "content": SYSTEM_INIT})
        insert_msg(
            user_id=user_id, role="system", content=SYSTEM_INIT, model="v3", used=used
        )
    else:
        # 获取历史记录
        msg = history
    msg.append({"role": "user", "content": question})
    insert_msg(user_id=user_id, role="user", content=question, model="v3", used=used)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=msg,
        stream=True,
        temperature=0.5,
    )

    ai_content = ""
    for chunk in response:
        if (
            hasattr(chunk.choices[0].delta, "content")
            and chunk.choices[0].delta.content
        ):
            content = chunk.choices[0].delta.content
            ai_content += content
            yield f"data:{content}\n\n"

    row = insert_msg(
        user_id=user_id, role="assistant", content=ai_content, model="v3", used=used
    )
    if not row:
        yield f"data:[ERROR]\n\n"
    yield f"data:[END]\n\n"


def R1_model(
    used,
    question="生成一段舒心的诗，500字以内",
    SYSTEM_INIT="你是一个深度思考的AI助手(R1模型)，擅长逻辑推理和深入分析。",
):
    client = OpenAI(
        api_key="sk-709b1426f00d42c880e1db9b43b22a3c",
        base_url="https://api.deepseek.com",
    )
    # 从数据库中获取历史记录
    user_id = information.get("data", {}).get("id")
    history = getHistory(user_id=user_id, used=used)
    msg = []
    if not history or SYSTEM_INIT != "你是一个有趣的AI助手，擅长日常问题的回答":
        msg.append({"role": "system", "content": SYSTEM_INIT})
        insert_msg(
            user_id=user_id, role="system", content=SYSTEM_INIT, model="r1", used=used
        )
    else:
        # 获取历史记录
        msg = history
    msg.append({"role": "user", "content": question})
    insert_msg(user_id=user_id, role="user", content=question, model="r1", used=used)
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=msg,
        stream=True,
    )
    ai_reasoning_content = ""
    reasoning_contents = ""
    yield "data:[THINKING]\n\n"
    thinking_complated = False
    for chunk in response:
        if (
            hasattr(chunk.choices[0].delta, "reasoning_content")
            and chunk.choices[0].delta.reasoning_content
        ):
            ai_reasoning_content += chunk.choices[0].delta.reasoning_content
            yield f"data:[THINKING]{chunk.choices[0].delta.reasoning_content}\n\n"

        if (
            hasattr(chunk.choices[0].delta, "content")
            and chunk.choices[0].delta.content
        ):
            if not thinking_complated:
                yield "data:[THINKING_END]\n\n"
                thinking_complated = True
            reasoning_contents += chunk.choices[0].delta.content
            yield f"data:{chunk.choices[0].delta.content}\n\n"
    insert_msg(
        user_id=user_id,
        role="assistant",
        content=f"[思考过程] {ai_reasoning_content} [最终输出] {reasoning_contents}",
        model="r1",
        used=used,
    )
    # 这里不再操作 session，只返回数据
    yield "data:[END]\n\n"


# 深思考问答接口


@app.route("/ask", methods=["GET"])
def ask_question():

    try:
        data = request.args
        question = data.get("q", "").strip()
        sys_init = data.get("sys_init", "").strip()
        model = data.get("model", "v3").strip()
        used = data.get("used", "ask")

        if not question:
            return jsonify({"error": "问题不能为空"}), 400
        SYSTEM_INIT = f"{sys_init}，现在的日期是{dt.datetime.now()}"

        if model == "v3":
            return Response(
                V3_model(question=question, SYSTEM_INIT=SYSTEM_INIT, used=used),
                mimetype="text/event-stream",
            )
        elif model == "r1":

            return Response(
                R1_model(question=question, SYSTEM_INIT=SYSTEM_INIT, used=used),
                mimetype="text/event-stream",
            )
        else:
            return Response("无效的模型", mimetype="text/event-stream")
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API请求失败: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"处理失败: {str(e)}"}), 500


# AI写作
@app.route("/api/aiWrite", methods=["GET"])
def ai_write():
    try:
        data = request.args
        model = data.get("model", "v3")
        title = data.get("title")
        content_id = data.get("content_type")
        tips = data.get("content")
        used = data.get("used", "write")
        if title is None or tips is None:
            return jsonify({"code": 0, "msg": "标题或者提示不能为空"}), 400
        # 定义AI角色
        content_type = getContentTypeById(content_id)
        SYSTEM_INIT = f"""
            角色描述  

            角色名称：AI 写作助手  

        一、核心功能：  
            1.多类型文章创作：根据用户提供的标题（{title}）、内容类型（{content_type}）和提示（{tips}）生成高质量文章。  

            2.字数控制：当用户没有指定字数（中文字符）要求时，默认输出 800-1200 中文字符。  

        二、技术文档优化：  
            当类型为技术类时，你的定位为代码小能手；优化技术文档的格式和结构，提高可读性。  

            1.代码块使用 <code> 标签包裹，并标注语言类型（如 <code language="python">）。  

            2.确保代码与正文排版清晰，增强可读性。  
            格式规范：  

            3.禁止使用 Markdown 语法，但是可以使用HTML语言中标签（但是不能包括HTML、Body等结构标签）

            4.技术类文档需优化段落、标题和代码块的排版结构。  
            5.内容安全：自动过滤敏感词汇，确保输出合规。  
            
        三、技术文档规范：  

            1.代码示例需完整、可运行（如适用）。  

            2.技术术语解释准确，避免歧义。  
            
            输出示例：  
            本文介绍 Python 的基本语法。以下是示例代码：  
            <code language="python">
            def hello_world():
                print("Hello, World!")
            </code>
            其中，空格使用html的实体转义符替换，换行使用<br>，TAB使用&nbsp;，如果需要在标签中使用样式，
            比如:
                <div style="color:red;"> This a div <div>
            必须结构需要清楚，不能出现标签名和属性黏在一块：<divstyle="color:red;"> This a div <div>
      四、内容要求：  
            
            无论任何类型的文章，必须逻辑性与连贯性：文章结构清晰，论点明确，行文流畅。  

            适用场景：  
            技术教程、学术论文、商业文案、创意写作等各类文本生成需求。  

            约束条件：  
            1.严格禁用 Markdown。  
            2.代码必须通过 <code> 标签标注语言类型。  
            3.不生成任何敏感或违规内容。  
            4.无论什么类型的文章，都需要优化排版
            5.无论什么类型的文章，换行使用<br>，如果需要分点则使用ul或者ol，段落使用p标签，段落的首字符缩进两个字符。
            标题使用h2标签。
    """

        if model == "v3":
            return Response(
                V3_model(question=tips, SYSTEM_INIT=SYSTEM_INIT, used=used),
                mimetype="text/event-stream",
            )
        elif model == "r1":
            return Response(
                R1_model(question=tips, SYSTEM_INIT=SYSTEM_INIT, used=used),
                mimetype="text/event-stream",
            )

        else:
            return """
                        <script>
                            alert("请选择正确的模型");
                        </script>
                """
    except requests.exceptions.RequestException as e:
        return jsonify({"code": 0, "msg": f"API请求失败: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"code": 0, "msg": f"处理失败: {str(e)}"}), 500


# 用户协议路由
@app.route("/agreement", methods=["GET"])
def agreement():
    return render_template("agreement.html")


# 检查内容是否含有敏感词
@app.route("/checkCotentisVaild", methods=["POST"])
def checkCotentisVaild():
    import os

    path = os.getcwd()
    sensitive_words = []
    try:
        with open(os.path.join(path, "SensitiveWords.txt"), "r", encoding="utf-8") as f:
            content = f.read()
            # 去除首尾空格和换行，然后按逗号分割，再去除每个词的单引号和空格
            sensitive_words = [w.strip().strip("'") for w in content.strip().split(",")]
    except Exception as e:
        print(f"发生错误：{str(e)}")
        return jsonify(
            {
                "code": 0,
                "msg": "敏感词文件加载失败~请联系管理员进行修复。预计修复时间：1小时内",
            }
        )
    finally:
        print("checkCotentisVaild() finally")
    content = request.get_json().get("content", "").lower()
    title = request.get_json().get("title", "").lower()
    for w in sensitive_words:
        if w in content:
            return jsonify({"code": 0, "msg": "含有敏感词，请修改后再提交！"})
        if w in title:  # 敏感词在标题中
            return jsonify(
                {
                    "code": 0,
                    "msg": "标题含有敏感词，请修改后再提交！",
                }
            )
    return jsonify({"code": 1, "msg": "内容合法"})


# ------------------------------------------- 其他路由 ---------------------------------------------------
# ------------------------------------------- 其他路由 ---------------------------------------------------
# 下载AIP
@app.route("/download_file/<int:title_id>/<path:filename>", methods=["GET"])
def downloadFile(title_id: int, filename: str):

    uploads = os.path.join(
        os.path.dirname(__file__), "upload", "attachment", f"user_{title_id}_attachment"
    )
    print(f"downloadFile() => {uploads}\\{filename}")
    pathx = os.path.join(uploads, filename)

    # 检查文件是否存在
    if not os.path.exists(pathx):
        print("文件不存在")
        return render_template("404.html", msg="文件好像自己就丢了~")

    # 返回文件
    try:
        return send_from_directory(uploads, filename, as_attachment=True)
    except Exception as e:
        print(f"文件下载失败：{e}")
        return "<script>alert('文件下载失败！');window.history.back();</script>"


# 路由：提供静态图片服务
@app.route("/allimg/<path:filename>", methods=["GET"])
def serve_image(filename):
    uploads = os.path.join(os.path.dirname(__file__))
    print(f"serve_image() => {uploads}\\{filename}")
    # 检查文件是否存在
    pathx = os.path.join(uploads, filename)

    # 返回文件
    try:
        if not os.path.exists(pathx):
            return "<script>alert('图片加载失败.....');</script>"
        return send_from_directory(uploads, filename, as_attachment=False)
    except Exception as e:
        print(f"图片下载失败：{e}")
        return "<script>alert('图片加载失败.....');</script>"


if __name__ == "__main__":
    flask.run()
