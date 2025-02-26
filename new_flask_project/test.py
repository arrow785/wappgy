import hashlib
import itertools
import os.path
import string

import dbutils.pooled_db
import requests
from werkzeug.utils import secure_filename
from getCurrPath import getUploadPath, getCurrPath, img_curr_path
from sql_flask.mymysql import ConMySQL
from new_flask_project.mytools import get_time, randName


def generate_passwords(charset, max_length):
    """生成指定字符集和最大长度的所有可能组合"""
    for length in range(1, max_length + 1):
        for combination in itertools.product(charset, repeat=length):
            yield ''.join(combination)


def brute_force_md5(md5_hash, charset, max_length):
    """暴力破解MD5哈希值"""
    for password in generate_passwords(charset, max_length):
        hashed = hashlib.md5(password.encode()).hexdigest()
        if hashed == md5_hash:
            return password
    return None


if __name__ == '__main__':
    fl = secure_filename(fr'static\upload_img\16.jpg')
    con = ConMySQL().mSQL()
    print(con)

# 59957072ba0b6fd04b7fe17f464f4cbd
