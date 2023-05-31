from flask import redirect
import pymysql

from .config import (
    session_number
)

def connect_db(url=None):
    try:
        db = pymysql.connect(host='localhost',
                        user='root',
                        password='117124fdu!',
                        database='tape',
                        charset='utf8')
    except Exception as e:
        print("连接失败")
        if url:
            return redirect(url)
        else:
            return None
    return db
# 提交成绩到数据库
def sqlOperation(sql):
    db = connect_db()
    if not db:
        return "连接数据库失败导致的提交失败"
    # print("数据库连接成功！")
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return "提交成功，感谢您的积极参与！(*^▽^*)"
    except Exception as e:
        return "提交失败"
# 根据sql语句读取数据库，
# 并以元组形式返回数据库读取结果
def sqlRead(sql):
    db = connect_db()
    if not db:
        return None
    # print("数据库连接成功！")
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result
# 根据状态排列读取
def sqlRead_status(status):
    sql = '''SELECT * FROM words_table WHERE username="%s";''' % (status)
    ret = []
    result = sqlRead(sql)
    if result is None:
        return None
    for item in result:
        ret_item = {
            'id': item[0],
            'date': item[1],
            'username': item[2],
            'words': item[3]
        }
        ret.append(ret_item)
    return ret