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


# 获取天气
def getWearther():
    url = f'https://api.vvhan.com/api/weather'
    try:
        resp = reqs.get(url=url)
        if resp.status_code == 200:
            weather = dict(resp.json())
            return weather
        else:
            return f'未获取到数据，状态码:{resp.status_code}'
    except reqs.exceptions.RequestException as e:
        print(f'请求失败！=> {e}')