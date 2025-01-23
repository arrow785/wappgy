# 主程序
from sql_flask.settings import MyFlask
from flask import render_template, request, session, redirect, url_for, jsonify
from dao.index import *
from dao.login import *
from dao.manager import *
from dao.register import *
from dao.write import *
from dao.detailed import *
from tools.mytools import md5
from sql_flask.mymysql import ConMySQL
from tools.mytools import getImage, getNews, getWearther

flask = MyFlask(__name__)
app = flask.app
# 设置密钥
app.config['SECRET_KEY'] = 'lisi_55assdasw'

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
               
               
if __name__ == '__main__':
    flask.run()
