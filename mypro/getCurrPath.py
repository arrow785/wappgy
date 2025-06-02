import os, os.path


img_curr_path = r"static\upload_img"
bgc_curr_path = r"static\upload_img\bgc"


def createAvatarPath(lid):
    fupath = os.path.join(
        os.path.dirname(__name__), "static", "upload", "avatar", f"user_{lid}_avatar"
    )
    # 确保目录存在，如果不存在则创建
    os.makedirs(fupath, exist_ok=True)
    print(fupath)
    return fupath


def createBgcPath(lid):
    fupath = os.path.join(
        os.path.dirname(__name__), "static", "upload", "bgc", f"user_{lid}_bgc"
    )
    # 确保目录存在，如果不存在则创建
    os.makedirs(fupath, exist_ok=True)
    # print(fupath)
    return fupath


def createCoverPath(lid):
    fupath = os.path.join(
        os.path.dirname(__name__), "static", "upload", "cover_img", f"user_{lid}_cover"
    )
    os.makedirs(fupath, exist_ok=True)
    print(fupath)
    return fupath


def createAttachmentPath(lid):
    fupath = os.path.join(
        os.path.dirname(__name__),
        "upload",
        "attachment",
        f"user_{lid}_attachment",
    )
    # 确保目录存在，如果不存在则创建
    os.makedirs(fupath, exist_ok=True)
    print(fupath)
    return fupath


def getCurrPath(file_name):
    # 获取当前文件所在的目录路径
    currpath = os.path.join(os.path.dirname(__file__))
    # 返回当前文件所在的目录路径
    return currpath


# print(os.path.dirname(__file__))
# print(getUploadPath())
