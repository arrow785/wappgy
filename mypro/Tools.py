import requests as reqs
import base64
from sql_flask.MySQL_DB import ConMySQL
from getCurrPath import *
from werkzeug.utils import secure_filename

# 取消使用MD5加密，前端使用SHA256加密
# md5
# def md5(text: str):
#     mmd5 = hashlib.md5()
#     mmd5.update(text.encode('utf-8'))
#     return mmd5.hexdigest()

newConMysql = ConMySQL()


# 获取当前时间
def get_time():
    import time

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


# 使用公共API获取随机壁纸
def getImage():
    url = "https://api.vvhan.com/api/bing?type=json&rand=sj"
    try:
        resp = reqs.get(url=url)
        if resp.status_code == 200:
            image = resp.json()
            return image
        else:
            return f"未获取到数据，状态码:{resp.status_code}"
    except reqs.exceptions.RequestException as e:
        print(f"请求失败！=> {e}")
        print(f"请求URL=> {url}")


# 获取知乎热榜
def getNews():
    url = "https://api.vvhan.com/api/hotlist/pengPai"
    resp = reqs.get(url=url)
    try:

        if resp.status_code == 200:
            news = resp.json()
            From: str = news.get("name")
            Update: str = news.get("update_time")
            print(From, Update)
            datas: list = list(news.get("data"))[0:10]
            new_dict: dict = {"from": From, "update": Update, "data": datas}
            return new_dict
        else:
            return f"未获取到数据，状态码:{resp.status_code}"
    except reqs.exceptions.RequestException as e:
        print(f"请求失败！=> {e}")


# 获取经纬度
def getWearther():
    url = "https://uapis.cn/api/myip.php"
    try:
        resp = reqs.get(url=url)
        if resp.status_code == 200:
            weather = dict(resp.json())
            print(weather)
            return weather
        else:
            return f"getWearther() => 未获取到数据，状态码:{resp.status_code}"
    except reqs.exceptions.RequestException as e:
        print(f"getWearther() => 请求失败！=> {e}")


import os


# 更新系统中的头像
def update_system_avatar(imgfile, uid):
    img_path = save_avatar_img(imgfile, uid)
    print(f"update_system_avatar() => 保存的路径：{img_path}")
    return img_path


def update_system_bgc(imgfile, uid):
    bgc_path = save_bgc_img(imgfile, uid)
    return bgc_path


def update_system_cover(imgfile, uid):
    return save_cover_img(imgfile, uid)


def save_cover_img(imgfile, uid):
    fileName = f"cover_{secure_filename(imgfile.filename)[:2]}_{uid}.jpg"
    file_path = os.path.join(createCoverPath(), fileName)
    try:
        imgfile.save(file_path)
        return os.path.join(r"static\upload_img\cover_img", fileName)
    except Exception as e:
        print(f"save_cover_img() => 保存封面图片错误！=> {e}")
        return r"static\upload_img\cover_img\cover_mr.jpg"
    finally:
        print(f"save_cover_img() => 保存封面图片完成，路径：{file_path}")


def save_bgc_img(imgfile, uid):
    filename = f"bg_{secure_filename(imgfile.filename)[:2]}_{uid}.jpg"
    file_path = os.path.join(createBgcPath(), filename)
    print(f"save_bgc_img() => 保存的路径：{file_path}")
    try:
        imgfile.save(file_path)
        return os.path.join(bgc_curr_path, filename)
    except Exception as e:
        print(f"save_bgc_img() => 保存背景图片错误！=> {e}")
        return "xxx"


# 保存图片到系统
def save_avatar_img(file: str, login_username_id):
    # 解码Base64转为图片
    img: bytes = base64.b64decode(file.split(",")[1])
    file_name = f"{login_username_id}_avatar.jpg"
    input_path = os.path.join(getUploadPath(), file_name)
    input_path1 = os.path.join(img_curr_path, file_name)
    print(f"save_img() => {input_path}")
    with open(input_path, "wb+") as f:
        f.write(img)
        if os.path.exists(input_path):
            print(f"保存成功！ save_img() => {input_path}")
            return input_path1
        else:
            print(f"保存失败！ save_img() => {input_path}")


def get_avatar(username):
    print(f"get ==> {username}")
    try:
        with newConMysql.getConnect() as db:
            sql = "select avatar from users where username= %s"
            cur = db.cursor()
            cur.execute(sql, (username,))
            result = cur.fetchone()
            # 如果查询结果不为空，则返回头像路径
            return result["avatar"] if result else "static/upload_img/mr.png"
    except Exception as e:
        print(f"get_avatar() 获取头像错误！=> {e}")
    finally:
        print(f"get_avatar() => 获取头像完成，释放连接")


def get_bgc(username):
    sql = "select bg_img from users where username= %s"
    try:
        with newConMysql.getConnect() as db:
            cur = db.cursor()
            cur.execute(sql, (username,))
            result = cur.fetchone()
            print(f"get_bgc() => 查询到的数据：{result}")
            # 如果查询结果不为空，则返回头像路径
            return result["bg_img"] if result else r"/static/upload_img/bgc/mr_bg2.jpg"
    except Exception as e:
        print(f"get_bgc() 获取背景图片错误！=> {e}")
    finally:
        print(f"get_bgc() => 获取背景图片完成")


# 随机昵称生成
def randName():
    import random, string, time

    first_name: str = "arr"
    # 获取当前时间
    fulx: str = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))[-6:]
    # 随机生成5位字符
    salt: str = "".join(random.choices(string.ascii_letters + string.digits, k=16))[0:5]
    # 组合昵称
    full_nick = first_name + fulx + salt
    return full_nick


# 计算总页数
def totalPage(total_count, limit):
    if total_count % limit == 0:
        return int(total_count / limit)
        # 否则，返回 total_count // limit + 1，保证多余的数据也能够被分到一页
    else:
        return int((total_count // limit) + 1)
