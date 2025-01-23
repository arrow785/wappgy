import hashlib
import itertools
import string

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

# 示例：破解MD5哈希值
if __name__ == "__main__":
    target_hash = "59957072ba0b6fd04b7fe17f464f4cbd"  # 示例哈希值（对应明文"hello"）
    charset = string.ascii_lowercase + string.digits  # 字符集：小写字母 + 数字
    max_length = 5  # 最大密码长度

    print(f"开始暴力破解MD5哈希值：{target_hash}")
    result = brute_force_md5(target_hash, charset, max_length)

    if result:
        print(f"破解成功！明文为：{result}")
    else:
        print("未找到匹配的明文。")
    
# 59957072ba0b6fd04b7fe17f464f4cbd