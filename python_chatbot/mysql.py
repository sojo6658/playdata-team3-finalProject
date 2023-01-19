import pymysql
def insert_log(author_id, author, author_name, message_contents, keywords, return_code, return_message):
    db = pymysql.connect(host='localhost', port=3306, user='localuser', password='1234', db='chatbotBase', charset='utf8')
    try:
        with db.cursor() as curs:
            sql = """insert into author_log(author_id, author, author_name, message_contents, keywords, return_code, return_message) values (%s, %s, %s, %s, %s, %s, %s)"""
            curs.execute(sql, (author_id, author, author_name, message_contents, keywords, return_code, return_message))
        try:
            db.commit()
        except:
            print(author_id)
            print(author)
            print(author_name)
            print(message_contents)
            print(return_code)
            print(return_message)
            print('Log_commit 실패')
        else:
            print('Log_commit 성공')
    finally:
        db.close()
        
def select_reservation(author_id):
    db = pymysql.connect(host='localhost', port=3306, user='localuser', password='1234', db='chatbotBase', charset='utf8')
    try:
        with db.cursor() as curs:
            sql = """SELECT index_id, message_contents FROM author_log WHERE (author_id = %s and return_code = 1) and cancel = 0"""
            curs.execute(sql, (author_id))
            result = curs.fetchall()
            return result
    finally:
        db.close()

def update_reservation(index_id):
    db = pymysql.connect(host='localhost', port=3306, user='localuser', password='1234', db='chatbotBase', charset='utf8')
    try:
        with db.cursor() as curs:
            sql = """UPDATE author_log SET cancel = 1 WHERE index_id = %s"""
            curs.execute(sql, (index_id))
        try:
            db.commit()
        except:
            print(index_id)
            print('Log_commit 실패')
        else:
            print('Log_commit 성공')
    finally:
        db.close()        
        
def select_column_table(column, table):
    db = pymysql.connect(host='localhost', port=3306, user='localuser', password='1234', db='chatbotBase', charset='utf8')
    try:
        with db.cursor() as curs:
            sql = """SELECT %s FROM %s """
            curs.execute(sql, (column, table))
            result = curs.fetchall()
            return result
    finally:
        db.close()
        
        
       