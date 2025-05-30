import os, os.path


img_curr_path = r"static\upload_img"
bgc_curr_path = r"static\upload_img\bgc"


def getUploadPath():
    fupath = os.path.join(os.path.dirname(__file__), r"static\upload_img")

    print(fupath)
    return fupath


def createBgcPath():
    fupath = os.path.join(os.path.dirname(__file__), r"static\upload_img\bgc")

    print(fupath)
    return fupath


def getCurrPath(file_name):
    # 获取当前文件所在的目录路径
    currpath = os.path.join(os.path.dirname(__file__))
    # 返回当前文件所在的目录路径
    return currpath


print(os.path.dirname(__file__))
print(getUploadPath())
