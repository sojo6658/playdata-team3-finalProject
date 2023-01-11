import pymysql
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# DB 연결 - db 정보 업데이트 필요
connection = pymysql.connect(host='localhost', port=3306, user='localuser', password='1234', db='chatbotBase', charset='utf8')
# db에서 데이터 추출하여 데이터프레임으로 저장
with connection.cursor() as cursor:
    sql = "SELECT uuid, url, course_data, course, categorie, keyword, course_info FROM chat_bot00"
    cursor.execute(sql)  
    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows)
#     print(df.head())
# 데이터프레임 컬럼명 변경
df.columns = ['uuid', 'url', 'course_data', 'course', 'categorie', 'keyword', 'course_info']
connection.close()
vectorizer = TfidfVectorizer()
# input sentence와 제일 유사한 아이템 내림차순 정렬 함수
def get_similar_documents(dataframe, input_sentence):
    # input sentence 벡터화
    input_vector = vectorizer.transform([input_sentence])

    # input vector와 입력된 DataFrame의 vectors 값 유사도 계산
    dit = dict()
    for idx, x in enumerate(cosine_similarity(input_vector.toarray(), dataframe['vectors'].tolist())[0]):
        dit[idx] = x
        
    # 유사도 높은 순으로 데이터프레임 내림차순 정렬
    dataframe = dataframe.iloc[[x[0] for x in sorted(dit.items(), key=lambda x : x[1], reverse=True)]]
    return dataframe
# 랭킹 점수 부여 함수
def dataframe_rank(df):
    df['rank'] = 0
    for i in range(len(df)):
        df['rank'][i] = len(df) - i
    return df
# get_similar_documents 함수 적용
# df3: 강좌명, df4: 카테고리, df5: 키워드, df6: 강의 정보

def recommendation(input_sentence):
    
    df3 = df[['uuid', 'course']].copy()
    df4 = df[['uuid', 'categorie']].copy()
    df5 = df[['uuid', 'keyword']].copy()
    df6 = df[['uuid', 'course_info']].copy()
    
    # TfidfVectorizer 로 문서 벡터화
    vectors4 = vectorizer.fit_transform(df6['course_info']) # 1360
    vectors = vectorizer.transform(df3['course']) # 1172
    vectors2 = vectorizer.transform(df4['categorie']) # 58
    vectors3 = vectorizer.transform(df5['keyword']) # 412
    
    # 데이터프레임에 벡터 보관용 컬럼 추가
    df3['vectors'] = list(vectors.toarray())
    df4['vectors'] = list(vectors2.toarray())
    df5['vectors'] = list(vectors3.toarray())
    df6['vectors'] = list(vectors4.toarray())
    
    df3 = get_similar_documents(df3, input_sentence)
    df4 = get_similar_documents(df4, input_sentence)
    df5 = get_similar_documents(df5, input_sentence)
    df6 = get_similar_documents(df6, input_sentence)

    df3.reset_index(drop=True, inplace=True)
    df4.reset_index(drop=True, inplace=True)
    df5.reset_index(drop=True, inplace=True)
    df6.reset_index(drop=True, inplace=True)
    
    # 랭킹 점수 부여 함수 적용
    df3 = dataframe_rank(df3)
    df4 = dataframe_rank(df4)
    df5 = dataframe_rank(df5)
    df6 = dataframe_rank(df6)
    
    # 강좌명, 카테고리, 키워드, 강의 정보 랭킹 점수 합산

    df3.sort_values(by='uuid', inplace=True)
    df4.sort_values(by='uuid', inplace=True)
    df5.sort_values(by='uuid', inplace=True)
    df6.sort_values(by='uuid', inplace=True)

    df3.reset_index(drop=True, inplace=True)
    df4.reset_index(drop=True, inplace=True)
    df5.reset_index(drop=True, inplace=True)
    df6.reset_index(drop=True, inplace=True)

    df_ranked = df[['uuid', 'url', 'course_data']].copy()
    df_ranked['rank_course'] = df3['rank']
    df_ranked['rank_category'] = df4['rank']
    df_ranked['rank_keyword'] = df5['rank']
    df_ranked['rank_course_info'] = df6['rank']

    df_ranked['rank_sum'] = df_ranked['rank_course'] + df_ranked['rank_category'] + df_ranked['rank_keyword'] + df_ranked['rank_course_info']
    df_ranked.sort_values(by='rank_sum', ascending=False, inplace=True)
       
    return df_ranked['url'][:5]