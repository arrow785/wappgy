import hashlib
import requests as reqs

# md5
def md5(text:str):
    mmd5 = hashlib.md5()
    mmd5.update(text.encode('utf-8'))
    return mmd5.hexdigest()


# 获取当前时间
def get_time():
    import time
    return time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))

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
            From:str = news.get('name')
            Update:str = news.get('update_time')
            print(From,Update)
            datas:list = list(news.get('data'))[0:10]
            new_dict:dict = {}
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
            return weather
        else:
            return f'未获取到数据，状态码:{resp.status_code}'
    except reqs.exceptions.RequestException as e:
        print(f'请求失败！=> {e}')
        
def save_image(imgfile,curr_path,username):
    import os
    from werkzeug.utils import secure_filename
    from sql_flask.mymysql import ConMySQL
    
    upload_folder = os.path.join(os.path.dirname(curr_path),r'static\upload_img')
    print(upload_folder)
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        
    file_name = secure_filename(imgfile.filename)
    # 拼接完整的文件路径
    full_path = os.path.join(upload_folder, file_name)
    # 将文件保存到指定路径
    imgfile.save(full_path)
    con,cur = ConMySQL().mSQL()
    try:
        with cur as c:
            sql = 'insert into avatar (id,username,avatar) values (default,%s,%s)'
            c.execute(sql,(username,full_path))
        con.commit()
    finally:
        cur.close()
        con.close()

def get_avatar(username):
    from sql_flask.mymysql import ConMySQL
    con,cur = ConMySQL().mSQL()
    try:
        with cur as c:
            sql = 'select avatar from avatar where username=%s'
            c.execute(sql,(username,))
            result = c.fetchone()
            # 如果查询结果不为空，则返回头像路径
            if result:
                return result['avatar']
            else:
                return 'xxx'
    finally:
        cur.close()
        con.close()
    