from konlpy.tag import Komoran
import pandas as pd

def get_pos(txt):
    dicpath = 'total_tabNNB.csv' # 텍스트 파일주소로, 사용자 사전의 구조는 위와 같습니다.
    kom = Komoran(userdic=dicpath)
    return kom.pos(txt, flatten=False, join=True)

def get_nouns(txt):
    dicpath = 'total_tabNNB.csv' # 텍스트 파일주소로, 사용자 사전의 구조는 위와 같습니다.
    kom = Komoran(userdic=dicpath)
    return kom.nouns(txt)

def get_nouns_text(txt):
    dicpath = 'total_tabNNB.csv' # 텍스트 파일주소로, 사용자 사전의 구조는 위와 같습니다.
    kom = Komoran(userdic=dicpath)
    user_output=''
    data_temp_list = kom.nouns(txt)
    for data_temp in data_temp_list:
        if data_temp_list[-1] == data_temp:
            user_output += data_temp
        else:
            user_output += data_temp + ', '
    return user_output

# def filter_my_dictionary(user_input):
#     filier_df=pd.read_csv('./total_set.csv')
#     word_data=[]
#     for word in get_nouns(str(user_input)):
#         word_data.append(word)
#     data_temp_list = filier_df[filier_df['.NET'].isin(word_data)].values.tolist()
#     user_output=''
    # for data_temp in data_temp_list:
    #     user_output += data_temp[0] + ', '        
    # return user_output[:-2]