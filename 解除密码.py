"解除所有PDF的密码"
import allpath
import os.path as op
import os
import PyPDF2
import sqlite3

SOURCE_NAME = allpath.DESTINATION_NAME
MY_DB_PATH = allpath.MY_DB_PATH
NAME = allpath.NAME

a = 0


# 遍历文件夹，返回文件列表
def travFloder():
    a = list()
    for item in os.walk(SOURCE_NAME):
        if item[2]:
            for item1 in item[2]:
                a.append(item[0]+'\\'+item1)
    return a


# 从数据库中获取密码
def getPasswd():
    with sqlite3.connect(MY_DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT 路径,密码 FROM data WHERE 课程名='{}'".format(NAME))
        values = c.fetchall()
        result = dict()
        for item in values:
            result[op.basename(item[0])] = item[1]
        return result


# 解除单个pdf密码
def rmPasswd(path, passwd):  # passwd:密码，path：绝对路径
    # 以读方式打开PDF文件
    PDFReader = PyPDF2.PdfFileReader(path)
    try:
        # 输入密码
        PDFReader.decrypt(passwd)
        # 实例化一个PDF写对象
        PDFWriter = PyPDF2.PdfFileWriter()
        # 将读对象的内容写入写对象
        PDFWriter.appendPagesFromReader(PDFReader)
        # 覆盖写入原PDF文件,实现解密
        PDFWriter.write(open(path, 'wb'))

        global a
        a = a+1
        print('{}\r'.format(a), end='')
    except:
        print(path)


# 主要操作,解除所有文件密码
def operate():
    files = travFloder()
    allpasswd = getPasswd()
    for file in files:
        # 获取文件名
        name = op.basename(file)
        # 获取密码
        passwd = allpasswd[name]
        # 解密
        rmPasswd(file, passwd)


if __name__ == "__main__":
    path = r'7_WS10单元学习资料.pdf'
    passwd = 'c604c133-04a2-46e7-a0d3-06856ee3befa'

    print(path)
    print(passwd)

    PDFReader = PyPDF2.PdfFileReader(path)
    # 输入密码
    PDFReader.decrypt(passwd)
    # 实例化一个PDF写对象

    PDFWriter = PyPDF2.PdfFileWriter()
    #  将读对象的内容写入写对象
    PDFWriter.appendPagesFromReader(PDFReader)
    # 覆盖写入原PDF文件,实现解密
    PDFWriter.write(open(path, 'wb'))
