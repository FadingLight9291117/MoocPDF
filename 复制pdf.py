"复制pdf：通过数据库读取数据，将mooc目录下的文件复制到自己的目录"
import allpath
import os
import os.path as op
import shutil
import sqlite3

# 当前程序所在目录
THIS_PATH = allpath.THIS_PATH
# 自己存放中间数据的数据库
MY_DB_PATH = allpath.MY_DB_PATH
# 目标文件夹
NAME = allpath.NAME
# 目标文件夹目录
DESTINATION_NAME = allpath.DESTINATION_NAME


# 复制网络爬虫文件夹
def copy():
    # 取出目录,并分割
    s = str()
    with sqlite3.connect(MY_DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT 路径 FROM data WHERE 课程名='{}' LIMIT 1".format(NAME))
        result = c.fetchall()
        s = result[0][0].split('\\')

    # 获得name所在的下标
    for i, value in enumerate(s):
        if NAME in value:
            goal = i
            break
    # 下面是复制文件夹操作
    sourceName = str()
    for i, value in enumerate(s):
        if i == goal:
            sourceName += value
            break
        sourceName += value+'/'  # 得到源文件夹目录
    # 复制文件夹
    while True:
        if os.path.exists(DESTINATION_NAME) == False:
            shutil.copytree(sourceName, DESTINATION_NAME)
            print("复制成功")
            break
        else:
            shutil.rmtree(DESTINATION_NAME)
            print("删除目录")


if __name__ == "__main__":
    copy()
