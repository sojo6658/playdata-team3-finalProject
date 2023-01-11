import pymysql
def insert_log(author_id, author, author_name, message_contents, keyword, return_code, return_message):
    db = pymysql.connect(host='localhost', port=3306, user='localuser', password='1234', db='chatbotBase', charset='utf8')
    try:
        with db.cursor() as curs:
            sql = """insert into author_log values (%s, %s, %s, %s, %s, %s, %s)"""
            curs.execute(sql, (author_id, author, author_name, message_contents, keyword, return_code, return_message))
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
        
def select_column(column):
    result = ''
    db = pymysql.connect(host='localhost', port=3306, user='localuser', password='1234', db='chatbotBase', charset='utf8')
    try:
        with db.cursor() as curs:
            sql = """SELECT %s FROM chat_bot220"""
            curs.execute(sql, (column))
            result = curs.fetchall()
            return result
    finally:
        db.close()