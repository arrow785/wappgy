import hashlib, os
import requests as reqs
import base64
from werkzeug.utils import secure_filename
import getCurrPath as myp
from getCurrPath import getCurrPath, img_curr_path
from PIL import Image


# md5
def md5(text: str):
    mmd5 = hashlib.md5()
    mmd5.update(text.encode('utf-8'))
    return mmd5.hexdigest()


# 获取当前时间
def get_time():
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


# 使用公共API获取随机壁纸
def getImage():
    url = 'https://api.vvhan.com/api/bing?type=json&rand=sj'
    try:
        resp = reqs.get(url=url)
        if resp.status_code == 200:
            image = resp.json()
            return image
        else:
            return f'未获取到数据，状态码:{resp.status_code}'
    except reqs.exceptions.RequestException as e:
        print(f'请求失败！=> {e}')
        print(f'请求URL=> {url}')


# 获取知乎热榜
def getNews():
    url = 'https://api.vvhan.com/api/hotlist/pengPai'
    try:
        resp = reqs.get(url=url)
        if resp.status_code == 200:
            news = resp.json()
            From: str = news.get('name')
            Update: str = news.get('update_time')
            print(From, Update)
            datas: list = list(news.get('data'))[0:10]
            new_dict: dict = {}
            new_dict['from'] = From
            new_dict['update'] = Update
            new_dict['data'] = datas
            return new_dict
        else:
            return f'未获取到数据，状态码:{resp.status_code}'
    except reqs.exceptions.RequestException as e:
        print(f'请求失败！=> {e}')


# 获取经纬度
def getWearther():
    url = 'https://uapis.cn/api/myip.php'
    try:
        resp = reqs.get(url=url)
        if resp.status_code == 200:
            weather = dict(resp.json())
            print(weather)
            return weather
        else:
            return f'getWearther() => 未获取到数据，状态码:{resp.status_code}'
    except reqs.exceptions.RequestException as e:
        print(f'getWearther() => 请求失败！=> {e}')


# 删除历史头像
def delete_avatar(username):
    from sql_flask.mymysql import ConMySQL
    con, cur = ConMySQL().mSQL()
    print(f'当前用户为：{username}')

    try:
        with cur as c:
            sql = 'select avatar as path from admin where username = %s'
            c.execute(sql, (username,))
            paths = c.fetchone()
            print(f'delete_avatar() => 数据库查询到的地址：{paths}')
            path = paths.get('path')
            if os.path.exists(path):
                print(f'delete_avatar() => 头像为默认头像，无需删除！')
                return False
            else:
                os.remove(path)
                print(f'delete_avatar() => 删除头像成功！')
                return True
    except Exception as e:
        print(f'delete_avatar() => 删除头像错误！=> {e}')
    finally:
        cur.close()
        con.close()

import os

# 更新系统中的头像
def update_system_avatar(imgfile: str, username):
    delete_avatar(username)
    img_path = save_img(imgfile, username)
    return img_path



# 保存图片到系统
def save_img(file: str, login_username):
    # 解码Base64转为图片
    img: bytes = base64.b64decode(file.split(',')[1])
    file_name = f'{login_username}_avatar.jpg'
    input_path = os.path.join(img_curr_path, file_name)
    with open(input_path, 'wb+') as f:
        f.write(img)
        if os.path.exists(input_path):
            print(f'保存成功！ save_img() => {input_path}')
            return input_path
        else:
            print(f'保存失败！ save_img() => {input_path}')


def get_avatar(username):
    from sql_flask.mymysql import ConMySQL
    con, cur = ConMySQL().mSQL()
    print(f'get ==> {username}')
    try:
        with cur as c:
            sql = 'select avatar from admin where username= %s'
            c.execute(sql, (username,))
            result = c.fetchone()
            # 如果查询结果不为空，则返回头像路径
            if result:
                return result['avatar']
            else:
                return 'xxx'
    except Exception as e:
        print(f'get_avatar() 获取头像错误！=> {e}')
    finally:
        cur.close()
        con.close()


# 随机昵称生成
def randName():
    import random, string, time
    first_name: str = 'arr'
    fulx: str = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[-6:]
    # 随机生成5位字符
    salt: str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))[0:5]
    # 组合昵称
    full_nick = first_name + fulx + salt
    return full_nick
