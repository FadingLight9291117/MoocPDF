"读取mooc本地数据库，提取其中的数据，先存储在CSV文件中，然后再从csv文件中存储到自己的数据库"
import allpath
import sqlite3
import csv
import os.path as op


# 当前程序所在目录
THIS_PATH = allpath.THIS_PATH
# MOOC数据库目录
MOOC_DB_PATH = allpath.MOOC_DB_PATH
# 自己存放中间数据的数据库
MY_DB_PATH = allpath.MY_DB_PATH
# 创建的csv文件的目录
CSV_PATH = allpath.CSV_PATH


# 从Mooc客户端sqlite数据库中提取所需数据
# 并写入data.csv文件中
def readMoocDatabase(path=None):
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT CourseName,UnitName,Password,FilePath FROM TransferFile ORDER BY CourseName")
        result = c.fetchall()
        global CSV_PATH
        with open(CSV_PATH, 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['课程名', '文件名', '密码', '路径'])
            writer.writerows(result)


# 从data.csv文件中读取数据存入数据库data.db
def writeMyData(data=None):
    # 连接数据库
    with sqlite3.connect(MY_DB_PATH) as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS data(\
                id integer PRIMARY KEY AUTOINCREMENT,\
                课程名 varchar,\
                文件名 varchar,\
                密码 varchar,\
                路径 varchar UNIQUE)')

        # 读取csv文件
        with open(CSV_PATH, 'r', encoding='utf-8') as file:
            # 以dict形式读取csv
            reader = csv.DictReader(file)
            data = list()
            for item in reader:
                data.append((dict(item)))
            # 将数据插入数据库
            for item in data:
                # 异常处理，应对插入相同的数据时插入失败异常
                try:
                    c.execute("INSERT INTO data (课程名,文件名,密码,路径) values ('{}','{}','{}','{}')".format(
                        item['课程名'], item['文件名'], item['密码'], item['路径']))
                except:
                    continue
            # 事务提交
            conn.commit()

def operate():
    readMoocDatabase(path=MOOC_DB_PATH)
    writeMyData()

if __name__ == "__main__":
    operate()