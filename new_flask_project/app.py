# 主程序
from sql_flask.settings import MyFlask
from flask import render_template, request, session, redirect, url_for, jsonify,send_from_directory
from flask_mail import Mail,Message
from dao.index import *
from dao.login import *
from dao.manager import *   
from dao.register import *
from dao.write import *
from dao.detailed import *
from dao.email import *
import os

from sql_flask.mymysql import ConMySQL
from tools.mytools import *

flask = MyFlask(__name__)
app = flask.app

# 设置密钥
app.config['SECRET_KEY'] = 'lisi_55assdasw'

loginUser:dict = {}

msqk = ConMySQL()


def set_session(username, password):
    if username is None or password is None:
        session['username'] = 'd'
    session['username'] = username


@app.route('/', methods=['GET'])
def main():
    news = getNews()
    weather = getWearther().get('data')
    city = getWearther().get('city')
    return render_template('zy.html', username=session.get('username', 'd'), news=news, weather=weather, city=city)


@app.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    datas = select_all(page, msqk, per_page)
    total_articles = get_total_articles(msqk)
    print(f'总页数：{total_articles}，所有数据：{datas}')
    total_pages = (total_articles + per_page - 1) // per_page  # 计算总页数
    username = session.get('username', 'd')
    return render_template('index.html', **locals())


@app.route('/detalied/<int:title_id>', methods=['GET'])
def detalied(title_id: int):
    data = full_context(title_id, msqk)
    comments = by_id(title_id, msqk)
    print(title_id, data)
    username = session.get('username', 'd')
    return render_template('detalied.html', **locals())


@app.route('/login', methods=['GET'])
def login():
    username = session.get('username', 'd')
    return render_template('login.html', **locals())


# 登录功能
@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    md5pasword = md5(password)
    rows = check_user(username, md5pasword)
    if rows == 0:
        return """
                  <script>
                        alert('账户或者密码错误！')
                        location.assign('/login')
                  </script>
                  """
    elif rows == 1:
        set_session(username, md5pasword)
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
def write():
    username = session.get('username', 'd')
    return render_template('write.html', **locals())


@app.route('/submit_write', methods=['POST'])
def submit_write():
    data = request.form
    title = data.get('title')
    context = data.get('content')
    insert_context(title, context, session.get('username'))
    return redirect(url_for('index', page=1))


@app.route('/manager', methods=['GET'])
def manager():
    username = session.get('username')
    datas = select_all_context(username, sqldb=msqk)
    return render_template('manager.html', **locals())


@app.route('/edit/<int:title_id>', methods=['GET'])
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
    data = request.form
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    print(type(email))
    md5pasword = md5(password)
    rows = insert_user(username, email, md5pasword)
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
    return jsonify(url=url,title=title)


@app.route('/curr_weather',methods=['GET'])
def curr_weather():
    weather = getWearther()
    print(weather)
    return jsonify(weather)


@app.route('/reset_pwd',methods=['GET'])
def reset_pwd():
    return render_template('resetpwd.html')


@app.route('/check_username/<string:username>',methods=['GET'])
def check_username(username:str):
    rows = check_(username=username)
    if rows != 0:
        return jsonify(exists=False)
    else:
        return jsonify(exists=True)
    
@app.route('/reset_pwd1',methods=['POST'])
def reset_pwd1():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    row = resetPwd(new_pwd=password,username=username)
    if row is not None:
        return """
                <script>
                    alert('修改成功！')
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
               
@app.route('/pep_dev',methods=['GET'])
def pep():
    username = session.get('username','d')
    datas = select_all_context(username=username,sqldb=msqk)
    print(datas)
    if datas is not None:
        return render_template('dev_people.html',**locals())


@app.route('/people',methods=['GET'])
def people():

    username = session.get('username','d')
    datas = select_all_context(username=username,sqldb=msqk)
    contents = select_emial(username=username,sqldb=msqk)
    # 图片地址要求是相对地址
    avatar = get_avatar(username=username)
    avatar_url = ''
    if avatar != 'xxx':
        avatar_url = os.path.relpath(avatar,os.path.dirname(__file__))
    else:
        avatar_url = 'static/upload_img/mr.png'
    return render_template('people.html',**locals())

# 留言板
@app.route('/boards',methods=['GET'])
def boards():
    return render_template('guestbook.html')


# 联系我
@app.route('/callme',methods=['GET'])
def callme():
    username = session.get('username', 'd')
    loginUser['username'] = username
    data = selectAll(username)
    if data is not None:
        loginUser['username'] = data['username']
        loginUser['email'] = data['email']
    else:
        loginUser['username'] = 'd'
        loginUser['email'] = '未知邮箱'
    return render_template('callme.html',username=loginUser.get('username','d'),mail=loginUser.get('email'))


# 发送邮件
@app.route('/send_email',methods=['POST'])
def send_email():

    data = request.form
    name = data.get('username','未知用户')
    email:str = data.get('email')
    content = data.get('msg')

    print('===@@>',name,email,content)
    # 配置 Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.163.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'xttdfix@163.com'
    app.config['MAIL_PASSWORD'] = 'LVgPZrqcMmmWFUdq'
    mail = Mail(app)
    msg = Message(subject=f"来自{name}的留言",sender='xttdfix@163.com',recipients=['luoruiGeng@163.com'])
    msg.body = f"来自{name}({email})的留言：{content}"
    if insert_emial(username=name,email=email,content=content,sqldb=msqk) is not None:
            print('插入成功！')
    else:
        print('插入失败！')
    
    try:
        mail.send(msg)
        if update_emial(username=name,sqldb=msqk) is not None:
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
        print(e)
        return """
            <script>
                alert('发送失败！')
                location.assign('/callme')
            </script>
        """


@app.route('/update_info',methods=['POST'])
def update_info():
    data = request.form
    imgfile = request.files.get('imgf')
    save_image(imgfile=imgfile,curr_path=__file__,username=session.get('username','d'))
    print(type(imgfile))
    newnick = data.get('newnick')
    newemail = data.get('newemail')
    introduce = data.get('introduce')
    print(newnick,newemail,introduce)
    return jsonify(send=True)


if __name__ == '__main__':
    flask.run()
