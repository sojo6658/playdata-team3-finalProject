from konlpy.tag import Komoran
import pandas as pd
dicpath = 'total_set_add_NNB.csv' # 텍스트 파일주소로, 사용자 사전의 구조는 위와 같습니다.
kom = Komoran(userdic=dicpath)
def get_keywords(pos, without_tag=False):
    exclusion_tags = [ # 'NNB' 
    'JKS', 'JKC', 'JKO', 'JKB', 'JKG', 'JKV', 'NNG','NNP','SL','VCP',
    'JK', 'JKQ', 'VV', 'VA', 'VX', 'MAG','MAJ','NP',
    'VC','MM', 'MA', 'IC', 
    'JX', 'JC', 'JK', 
    'SF', 'SP', 'SS', 'SE', 'SO', 'SH', 'SW', 
    'NF', 'NV', 
    'SN', 'NA', 'EP', 'EF', 'EC', 'ETN', 'ETM', 
    'XSN', 'XSV', 'XSA', 'XPN', 'XR']
    f = lambda x: x in exclusion_tags
    word_list = []
    for p in pos:
        if f(p[1]) is False:
            if without_tag is False:
                word_list.append(p)
            else:
                word_list.append(p[0])
    return word_list
    
def get_keywords_true(pos, without_tag=True):
    exclusion_tags = [ # 'NNB' 
    'JKS', 'JKC', 'JKO', 'JKB', 'JKG', 'JKV', 'NNG','NNP','SL','VCP',
    'JK', 'JKQ', 'VV', 'VA', 'VX', 'MAG','MAJ','NP',
    'VC','MM', 'MA', 'IC', 
    'JX', 'JC', 'JK', 
    'SF', 'SP', 'SS', 'SE', 'SO', 'SH', 'SW', 
    'NF', 'NV', 
    'SN', 'NA', 'EP', 'EF', 'EC', 'ETN', 'ETM', 
    'XSN', 'XSV', 'XSA', 'XPN', 'XR']
    f = lambda x: x in exclusion_tags
    word_list = []
    for p in pos:
        if f(p[1]) is False:
            if without_tag is False:
                word_list.append(p)
            else:
                word_list.append(p[0])
    return word_list

def get_nouns_text(txt):
    user_output=''
    data_temp_list = kom.nouns(txt)
    for data_temp in data_temp_list:
        user_output += data_temp[0] + ', '        
    return user_output[:-2]

def filter_my_dictionary(user_input):
    filier_df=pd.read_csv('./dictionary_lower_split.csv') # 저희의 사전입니다 
    word_data=[]
    for word in get_keywords_true(kom.pos(user_input)):
        word_data.append(word.split())
    df_temp = pd.DataFrame(word_data)
    df_temp = df_temp[[0]]
    df_temp = df_temp.applymap(str.lower)
    data_temp_list = df_temp[df_temp[0].isin(filier_df['0'])].values.tolist()
    user_output=''
    for data_temp in data_temp_list:
        user_output += data_temp[0] + ', ' #파이썬, 기초
    if user_output == '':
        user_output = '   '
    return user_output[:-2]