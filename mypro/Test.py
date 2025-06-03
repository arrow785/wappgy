import datetime as dt


import os


# pathx = os.path.join(os.path.dirname(os.path.abspath(__file__)), "零时-Tencent.txt")
# print(pathx)
# sensitive_arr = []
# with open(pathx, "r", encoding="utf-8") as file:
#     # 通过换行符分割每一行
#     lines = file.read().strip().splitlines()
#     # 去除每行的首尾空格
#     lines = [line.strip() for line in lines]
#     # 过滤掉空行
#     lines = [line for line in lines if line]
#     # 打印每行内容
#     for line in lines:
#         sensitive_arr.append(line)

# print(len(sensitive_arr))


resx = len({"key": 1})
print(resx)

strx = """

宇宙的起源一直是人类探索的终极谜题之一。从古至今，科学家和哲学家们不断提出各种理论，试图解释这个浩瀚无垠的宇宙是如何形成的。虽然我们至今仍未完全揭开宇宙起源的全部秘密，但现代科学已经为我们提供了一些重要的线索和理论。 目前，最广为接受的宇宙起源理论是大爆炸理论。这一理论认为，宇宙最初是一个极其高温、高密度的奇点。大约在138亿年前，这个奇点发生了剧烈的爆炸，宇宙由此诞生。爆炸后的瞬间，宇宙开始迅速膨胀，温度逐渐降低，物质开始形成。最初的几分钟内，宇宙中只有最简单的元素——氢和氦，之后才逐渐形成了更复杂的元素和结构。 大爆炸理论并非凭空想象，而是基于多项科学观测和实验证据。例如，科学家发现了宇宙微波背景辐射，这是大爆炸后留下的余热，被认为是宇宙诞生的重要证据之一。此外，宇宙的膨胀现象也为大爆炸理论提供了支持。1929年，天文学家哈勃观察到遥远的星系正在远离我们，这表明宇宙正在膨胀。如果时间倒流，宇宙必然是从一个极小的点开始膨胀的。 然而，大爆炸理论并不能解释宇宙诞生之前的状态。科学家们仍在努力探索宇宙诞生之前的可能情况。一些理论认为，宇宙可能起源于量子涨落，即在真空中突然出现的能量波动导致了宇宙的形成。另一些理论则提出了“多元宇宙”的概念，认为我们的宇宙只是无数宇宙中的一个。这些理论虽然尚未被完全证实，但它们为我们理解宇宙的起源提供了新的视角。 宇宙的形成并非一蹴而就。大爆炸后，宇宙经历了漫长的演化过程。最初的几亿年里，宇宙中充满了炽热的等离子体，光线无法穿透。直到大约38万年后，宇宙冷却到足以让电子和原子核结合，形成了中性原子，光线才得以自由传播。这一阶段被称为“宇宙再电离时期”。随后，星系、恒星和行星开始逐渐形成。 恒星的形成是宇宙演化的重要环节。巨大的气体云在引力作用下坍缩，形成恒星。恒星内部的核聚变反应产生了更重的元素，如碳、氧、铁等。这些元素在恒星死亡时被抛洒到宇宙中，成为新一代恒星和行星的原料。我们的太阳系就是在这样的过程中形成的，地球上的所有物质都源自这些古老的恒星。 宇宙的起源和演化是一个复杂而神秘的过程。尽管我们已经有了一些重要的发现，但仍有许多未解之谜等待解答。例如，暗物质和暗能量的本质是什么？它们如何影响宇宙的膨胀和结构？这些问题仍然是现代天文学和物理学的研究重点。 人类对宇宙起源的探索不仅满足了我们的好奇心，也推动了科学技术的进步。通过研究宇宙的起源，我们更深刻地理解了自然规律，也为未来的科技发展提供了新的可能性。也许有一天，我们能够完全揭开宇宙起源的奥秘，但在此之前，探索的脚步永远不会停止。 宇宙的起源故事告诉我们，人类虽然是宇宙中微不足道的一部分，但我们拥有探索和思考的能力。正是这种能力，让我们能够一步步接近宇宙的真相。无论未来的发现如何，宇宙的起源始终是一个充满魅力和挑战的课题，激励着我们不断前进。

"""


# def vail(strx):
#     for sensitive_word in sensitive_arr:
#         if sensitive_word in strx:
#             return f"敏感词：{sensitive_word}"

#     return "没有敏感词"


# print(vail(strx))
import re, time, random
from werkzeug.utils import secure_filename

stex = """Java发展史：从Oak到云时代的演进Java的诞生可追溯至1991年。当时Sun公司的帕特里克·诺顿团队启动"Green项目"，旨在开发嵌入式系统语言。最初命名为Oak（橡树），后因商标问题于1995年正式更名为Java。
"""


def x(s):
    for i in s:
        x = random.uniform(0.025, 0.075)
        time.sleep(x)
        yield f"{i}"
    yield "data:end"


# for chunk in x(stex):
#     print(chunk, end="", flush=True)
newFileName = "JavaXXX.pdf"
pattern = re.compile(r"[\u4e00-\u9fff]").search(newFileName)
# 如果文件名中没有中文，则直接使用文件名
fileName = ""
if pattern is None:
    fileName = secure_filename(newFileName)
else:
    ch_filename = newFileName.split(".")
    fux = ch_filename[-1]  # 文件后缀
    fileName = ch_filename[0] + "_" + f".{fux}"

print(fileName)

lsj = [
    {"role": "system", "content": "你是一个AI助手"},
    {"role": "user", "content": "你好"},
]
newarr = []
arr = lsj.copy()
newarr = lsj.copy() if newarr else []
newarr.append({"role": "assistant", "content": "你好"})
newarr = lsj.copy() if newarr else []
print(newarr)

from sql_flask.MySQL_DB import ConMySQL
from Tools import get_time

newConMysql = ConMySQL()

history_arr = []
cur = newConMysql.getConnect().cursor()
cur.execute("select role,content from chat_history where user_id = 1")
res = cur.fetchall()
for i in res:
    history_arr.append(i)
print(history_arr)
cur.close()
tx = [
    {"role": "system", "content": "1+1=2？"},
    {"role": "assistant", "content": "1+1=2？"},
]
f = []
f = tx
print(f"f=>{f}")
