# 主程序

from functools import wraps

from sql_flask.settings import MyFlask
from flask import render_template, request, session, redirect, url_for, jsonify
from flask_mail import Mail, Message
from dao.index import *
from dao.user import *
from dao.manager import *
from dao.write import *
from dao.detailed import *
from dao.email import *

from sql_flask.mymysql import ConMySQL
from tools.mytools import *

flask = MyFlask(__name__)
app = flask.app

information: dict = {}
loginUser: dict = {}


@app.route('/totest', methods=['GET'])
def test1():
    return render_template('test.html')


@app.route('/test', methods=['POST'])
def test():
    pwd = request.form.get('password')
    print(f'test() => {pwd}')
    return 'dev'


# 登录装饰器
def my_login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Checking session:", session)  # 添加调试信息
        if session.get('username', 'd') == 'd':
            print("User not logged in, redirecting to main")
            return redirect(url_for('tologin'))
        else:
            print("User logged in, proceeding")
            return func(*args, **kwargs)

    return wrapper


# 设置密钥
def get_salt():
    import string, random
    salt: str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return salt


app.config['SECRET_KEY'] = get_salt()
# string随机盐生成

msqk = ConMySQL()


# 更新字典information的数据
def update_information(username):
    information['data'] = selectAll(username, msqk)
    print(f"update_information() 更新的内容为 => {information.get('data', {})}")


def set_session(username):
    session['username'] = username
    if username is None:
        session['username'] = 'd'
    else:
        update_information(username)
        print(information.get('data'))


@app.route('/', methods=['GET'])
def main():
    news = getNews()
    return render_template('zy.html', username=session.get('username', 'd'), news=news)


@app.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    datas = select_all(page, msqk, per_page)
    total_articles = get_total_articles(msqk)
    print(f'总页数：{total_articles}，所有数据：{datas}')
    total_pages = (total_articles + per_page - 1) // per_page  # 计算总页数
    username = session.get('username', 'd')
    # 获取用户头像
    avatar_path = get_avatar(username=username)
    return render_template('index.html', **locals())


@app.route('/detalied/<int:title_id>', methods=['GET'])
def detalied(title_id: int):
    data = full_context(title_id, msqk)
    comments = by_id(title_id, msqk)
    avatar_path = information.get('data', {}).get('avatar')
    print(title_id, data)
    print(comments)
    username = session.get('username', 'd')
    return render_template('detalied.html', **locals())


@app.route('/login', methods=['GET'])
def tologin():
    username = session.get('username', 'd')
    return render_template('login.html', **locals())


# 登录功能
@app.route('/login_sub', methods=['POST'])
def login():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    md5pasword = password
    rows = check_user(username, md5pasword)
    if rows == 0:
        return """
                  <script>
                        alert('账户或者密码错误！')
                        location.assign('/login')
                  </script>
                  """
    elif rows == 1:
        set_session(username)
        return """
                    <script>
                        location.assign('/index')
                    </script>
                """


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('main'))


@app.route('/comment_submit/<int:title_id>/<string:name>/<string:zhuti>', methods=['POST'])
def comment_submit(title_id: int, name: str, zhuti: str):
    print(title_id, name)
    comments = request.form.get('comment')
    insert_comment(name, comments, title_id, zhuti=zhuti, sqldb=msqk)
    return redirect(url_for('detalied', title_id=title_id))


@app.route('/write', methods=['GET'])
@my_login_required
def write():
    username = session.get('username', 'd')
    avatar_path = information.get('data', {}).get('avatar')
    return render_template('write.html', **locals())


@app.route('/submit_write', methods=['POST'])
def submit_write():
    data = request.form
    title = data.get('title')
    context = data.get('content')
    insert_context(title, context, session.get('username'))
    return redirect(url_for('index', page=1))


@app.route('/manager', methods=['GET'])
@my_login_required
def manager():
    username = session.get('username')
    datas = select_all_context(username, msqk)
    avatar_path = information.get('data', {}).get('avatar')
    return render_template('manager.html', **locals())


@app.route('/edit/<int:title_id>', methods=['GET'])
@my_login_required
def edit(title_id: int):
    datas = find_context(title_id)
    return render_template('edit.html', **locals())


@app.route('/submit_edit', methods=['POST'])
def submit_edit():
    datas = request.form
    title = datas.get('title')
    content = datas.get('content')
    title_id: int = int(datas.get('title_id'))
    print(title_id)
    rows = update_content(title_id=title_id, content=content, title=title)
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


@app.route('/delete/<int:t_id>', methods=['GET'])
def delete(t_id: int):
    print(f't_id==>{t_id}')
    rows = delete_context(t_id)
    flg = False
    if rows is not None:
        flg = True
    return jsonify(flg=flg)


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/submit_register', methods=['POST'])
def submit_register():
    if request.method == 'GET':
        return redirect(url_for('register'))
    data = request.form
    username = data.get('username')
    # 获取当前时间
    register_date = get_time()
    # 获取随机昵称
    nickName = data.get('nickname')
    if nickName is '':
        nickName = randName()
    password = data.get('password')
    email = data.get('email')
    print(f'submit_register() => : username==>{username},password==>{password},email==>{email},nickName==>{nickName}')
    md5pasword = password
    rows = insertUser(username=username, email=email, password=md5pasword,
                      register_date=register_date, nickName=nickName)
    if rows is not None:
        return """
                <script>
                    alert('注册成功！')
                    location.assign('/login')
                </script>
               """
    else:
        return """
                <script>
                    alert('注册失败！未知错误。')
                    location.assign('/register')
                </script>
               """


@app.route('/next', methods=['GET'])
def next1():
    imgUrl = getImage()
    url = imgUrl.get('data').get('url')
    title = imgUrl.get('data').get('title')
    return jsonify(url=url, title=title)


@app.route('/curr_weather', methods=['GET'])
def curr_weather():
    weather = getWearther()
    print(weather)
    return jsonify(weather)


@app.route('/reset_pwd', methods=['GET'])
def reset_pwd():
    return render_template('resetpwd.html')


# 注册时，判断用户名是否已经存在
@app.route('/check_username/<string:username>', methods=['GET'])
def check_username(username: str):
    rows = check_(username=username)
    print(f'check_username=>{username}')
    if rows != 0:
        return jsonify(exists=False)
    else:
        return jsonify(exists=True)


@app.route('/reset_pwd1', methods=['POST'])
def reset_pwd1():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    print(f'reset_pwd1() => : username==>{username},password==>{password}')
    row = resetPwd(new_pwd=password, username=username)
    if row is not None:
        return """
                <script>
                    alert('重置成功！')
                    location.assign('/login')
                </script>
               """
    else:
        return """
                <script>
                    alert('修改失败！未知错误，请联系开发者')
                    location.assign('/reset_pwd')
                </script>
               """


@app.route('/pep_dev', methods=['GET'])
def pep():
    datas = select_all_context(username='喜欢劈瓜的刘华强', sqldb=msqk)
    print(datas)
    if datas is not None:
        return render_template('dev_people.html', **locals())


# 留言板
@app.route('/boards', methods=['GET'])
def boards():
    datas = selectGuestContext(sqldb=msqk)
    username = session.get('username', 'd')
    return render_template('guestbook.html', **locals())


# 联系我

@app.route('/callme', methods=['GET'])
def callme():
    # 获取用户信息
    username = session.get('username', 'd')
    # print(username)
    loginUser['username'] = username
    return render_template('callme.html',
                           username=username)


# 发送邮件
@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.form
    content = data.get('msg')
    name = session.get('username', '游客1')
    email = data.get('email', {})
    if email == '':
        email = 'youke@youke@163.com'
    print(f'email => {type(email)}')
    print(f'email = > {email} , information = > {information}')
    print('===@@>', name, email, content)
    # 配置 Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.163.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'xttdfix@163.com'
    app.config['MAIL_PASSWORD'] = 'LVgPZrqcMmmWFUdq'
    mail = Mail(app)
    msg = Message(subject=f"来自{name}的留言", sender='xttdfix@163.com', recipients=['luoruiGeng@163.com'])
    msg.body = f"来自{name}({email})的留言：{content}"
    if insert_emial(username=name, email=email, content=content, sqldb=msqk) is not None:
        print('插入成功！')
    else:
        print('插入失败！')

    try:
        mail.send(msg)
        if update_emial(username=name, sqldb=msqk) is not None:
            print('更新成功！')
        else:
            print('更新失败！')
        return """
            <script>
                alert('发送成功！')
                location.assign('/callme')
            </script>

    """
    except Exception as e:
        print(f'send_email() error=> {e}')
        return """
            <script>
                alert('发送失败！')
                location.assign('/callme')
            </script>
        """


@app.route('/people', methods=['GET'])
@my_login_required
def people():
    print(f'people() == >被调用')
    username = session.get('username', 'd')
    ifm = information.get('data', {})
    print(f'ifm ==> {ifm}')
    contexts = select_all_context(username=username, sqldb=msqk)
    contents = select_emial(username=username)
    # 图片地址要求是相对地址
    avatar = get_avatar(username=username)
    print(avatar)
    if avatar == 'xxx':
        avatar = 'static/upload_img/mr.png'
    return render_template('people.html', **locals())


# 修改个人信息
@app.route('/update_info', methods=['POST'])
def update_info():
    data = request.form
    imgfile = data.get('croppedImage')
    name = session.get('username', 'd')

    print(f'类型：{type(imgfile)} 数据：=> {imgfile}')
    path = update_system_avatar(imgfile=imgfile,
                                uid=information.get('data', {}).get('id'))
    newnick = data.get('newnick')
    newemail = data.get('newemail')
    introduce = data.get('introduce')

    print(newnick, newemail, introduce)
    rows = update_user(username=session.get('username', 'd'), email=newemail, nickName=newnick, introduce=introduce,
                       avatar=path, sqldb=msqk)
    update_information(name)
    if rows is not None:
        return redirect(url_for('people'))
    else:
        return """
                <script>
                    alert('修改失败！未知错误，请联系开发者')
                    location.assign('/people')
                </script>
               """


@app.route('/update_pwd', methods=['post'])
def update_pwd():
    pwd = request.form.get('pwd')
    username = session.get('username', 'd')

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


@app.route('/checkoldpwd', methods=['POST'])
def checkoldpwd():
    oldPwd = getOldPwd(session.get('username', 'd'))
    newpwd = request.json.get('pwd1')
    print(oldPwd, newpwd)
    if oldPwd == newpwd:
        return jsonify(exists=True)
    return jsonify(exists=False)


@app.route('/show_information/<string:username>', methods=['GET'])
def show_information(username: str):
    data = show_info(username)
    contexts = select_all_context(username=username, sqldb=msqk)
    print(f'show_information() => {contexts}')
    return render_template('user_people.html', **locals())


@app.route('/guestbook', methods=['post'])
def guestbook():
    username = session.get('username', '游客')
    print(f'guestbook() => {username}')
    avatar_path = get_avatar(username=username)
    row = insertGuestContext(username=username, context=request.form.get('context'), avatar=avatar_path)
    if row is not None:
        return redirect(url_for('boards'))
    else:
        return """
                <script>
                    alert('留言失败！未知错误，请联系开发者')
                    location.assign('/boards')
                </script>
               """
@app.route('/show_version', methods=['GET'])
def show_version():
    return render_template('version.html')

if __name__ == '__main__':
    flask.run()
