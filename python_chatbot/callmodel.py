from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def get_similar_documents(input_sentence):
    df2 = pd.read_csv('./dataF01.csv')
    df2= df2.dropna(axis=0)
    df2['course'] = df2['course'].str.strip()
    df2['course'] = df2['course'].str.replace(',',' ')
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(df2['course'])
    df2['vectors'] = list(vectors.toarray())
    df=df2.copy()
    # Convert the input sentence into a vector
    input_vector = vectorizer.transform([input_sentence.replace(',',' ')])

    # Calculate the similarity between the input vector and the vectors in the DataFrame
    dit = dict()
    for idx, x in enumerate(cosine_similarity(input_vector.toarray(), df2['vectors'].tolist())[0]):
        dit[idx] = x 
        
    # Return the top 5 most similar documents
    print(input_sentence.replace(',',' '))
    print(df.iloc[[x[0] for x in sorted(dit.items(), key=lambda x : x[1])[-5:]]]['course'])
    return df.iloc[[x[0] for x in sorted(dit.items(), key=lambda x : x[1])[-5:]]]['url']

def get_URL(user_input):
    return_df= get_similar_documents(user_input)
    val_list = return_df.values.tolist()
    return(val_list)