import requests as reqs
import base64
from sql_flask.MySQL_DB import ConMySQL
from getCurrPath import *
from werkzeug.utils import secure_filename

import os

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


# 创建头像图片存储路径
def save_avatar_to_system(imgfile, lid):
    img_path = save_avatar_img(imgfile, lid)
    print(f"update_system_avatar() => 保存的路径：{img_path}")
    return img_path


# 保存头像图片到系统
def save_bgc_to_system(imgfile, lid):
    bgc_path = save_bgc_img(imgfile, lid)
    return bgc_path


# 创建封面图片存储路径，并保存封面图片
def save_cover_to_system(imgfile, lid):
    if not imgfile:
        print("save_cover_to_system() => 使用默认封面图片")
        return r"static\upload\cover_img\user_mr_cover\cover_mr.jpg"
    return save_cover_img(imgfile, lid)


def save_cover_img(imgfile, lid):
    date = "-".join(get_time().split("-")[:2])
    fileName = f"cover_{lid}_{date}_{secure_filename(imgfile.filename)}"
    file_path = os.path.join(createCoverPath(lid), fileName)
    try:
        imgfile.save(file_path)
        return file_path
    except Exception as e:
        print(f"save_cover_img() => 保存封面图片错误！=> {e}")
        return r"static\upload\cover_img\user_mr_cover\cover_mr.jpg"
    finally:
        print(f"save_cover_img() => 保存封面图片完成，路径：{file_path}")


# 创建背景图片存储路径
def save_bgc_img(imgfile, lid):
    date = "-".join(get_time().split("-")[:2])
    filename = f"bg_{lid}_{date}_{secure_filename(imgfile.filename)}"
    file_path = os.path.join(createBgcPath(lid), filename)
    print(f"save_bgc_img() => 保存的路径：{file_path}")
    try:
        imgfile.save(file_path)
        return file_path
    except Exception as e:
        print(f"save_bgc_img() => 保存背景图片错误！=> {e}")
        return r"static\upload\bgc\user_mr_bgc\mr_bg2.jpg"


# 保存图片到系统
def save_avatar_img(file: str, lid):
    # 解码Base64转为图片
    img: bytes = base64.b64decode(file.split(",")[1])
    file_name = f"{lid}_avatar.jpg"
    input_path = os.path.join(createAvatarPath(lid=lid), file_name)
    # input_path1 = os.path.join(img_curr_path, file_name)
    print(f"save_img() => {input_path}")
    try:
        with open(input_path, "wb+") as f:
            f.write(img)
            if os.path.exists(input_path):
                print(f"保存成功！ save_img() => {input_path}")
                return input_path
            else:
                return r"static\upload\avatar\user_mr_avatar\avatar_mr.png"
    except Exception as e:
        print(f"save_img() => 保存图片错误！=> {e}")
        return r"static\upload\avatar\user_mr_avatar\avatar_mr.png"


#  获取头像，但是弃用
def get_avatar(username):
    print(f"get ==> {username}")
    try:
        with newConMysql.getConnect() as db:
            sql = "select avatar from users where username= %s"
            cur = db.cursor()
            cur.execute(sql, (username,))
            result = cur.fetchone()
            # 如果查询结果不为空，则返回头像路径
            return (
                result["avatar"]
                if result
                else r"upload\avatar\user_mr_avatar\mr_avatar.jpg"
            )

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
            return result["bg_img"] if result else r"upload\bgc\user_mr_bgc\mr_bg2.jpg"
    except Exception as e:
        print(f"get_bgc() 获取背景图片错误！=> {e}")
    finally:
        print(f"get_bgc() => 获取背景图片完成")


# 随机昵称生成
def randName():
    import random, string, time

    first_name: str = "USER_"
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


# 保存附件
def save_attachment(files, title_id):
    import re

    paths = []
    date = "-".join(get_time().split("-")[:2])
    file_path = ""
    # 检查文件是否为空
    if files[0].filename == "":
        return None
    try:
        for file in files:
            # 如果文件名中有逗号，则替换为下划线
            newFileName = file.filename.replace(",", "_").replace(" ", "_")
            fileName = ""
            pattern = re.compile(r"[\u4e00-\u9fff]").search(newFileName)
            # 如果文件名中没有中文，则直接使用文件名
            if pattern is None:
                fileName = secure_filename(newFileName)
            else:
                ch_filename = file.filename.split(".")
                fux = ch_filename[-1]  # 文件后缀
                fileName = ch_filename[0] + f".{fux}"

            file_path = os.path.join(
                createAttachmentPath(title_id),
                f"{title_id}-{date}-{fileName}",
            )
            file.save(file_path)
            print(f"save_attachment() => 保存附件成功！路径：{file_path}")
            paths.append(file_path)
        return ",".join(paths)
    except (Exception, FileNotFoundError) as e:
        print(f"save_attachment() => 保存附件错误！=> {e}")
        return None
    finally:
        print(f"save_attachment() => 保存附件完成，路径：{file_path}")


# 导入
from openai import OpenAI
from flask import session


# AI流式输出 R1
