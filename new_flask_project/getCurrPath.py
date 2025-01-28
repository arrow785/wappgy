import os, os.path


img_curr_path = fr'static\upload_img'
def getUploadPath():
    fupath = os.path.join(os.path.dirname(__file__), r'static\upload_img')
    print(fupath)
    return fupath



def getCurrPath(file_name):
    currpath = os.path.join(os.path.dirname(__file__))
    return currpath


print(os.path.dirname(__file__))
print(getUploadPath())
