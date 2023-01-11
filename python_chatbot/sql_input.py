import pymysql
db = pymysql.connect(host='localhost', port=3306, user='localuser', password='1234', db='chatbotBase', charset='utf8')
result = ''
try:
    with db.cursor() as curs:
        sql = "SELECT course_data FROM chat_bot2"
        curs.execute(sql)
        result = curs.fetchall()
finally:
    db.close()
    
count=0

for course_data in result:
    count+=1
    if count
    