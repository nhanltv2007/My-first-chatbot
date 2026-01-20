import json
import numpy as np
from gensim.models import Word2Vec
from numpy.linalg import norm
import Tokenization

# model = Word2Vec(
#     sentences=  data,
#     vector_size = 200,
#     window=5,
#     min_count=3,
#     sg=1,
#     negative=10,
#     sample=1e-3,
#     epochs=5,
#     workers=4
# )
# model.save("Word2Vec.model")
model =None
def load_model():
    global model
    if model is None:
        model = Word2Vec.load("Word2Vec.model")

# vectorizer = TfidfVectorizer(
#     tokenizer=lambda x: x,
#     preprocessor=lambda x:x,
#     token_pattern= None,
#     lowercase = False
#                              )
# vectorizer.fit(data)  # data = list các câu (đã tokenize)
# #
# # # Tạo tfidf
# tfidf = dict(zip(
#     vectorizer.get_feature_names_out(),
#     vectorizer.idf_
# ))

# # Lưu tfidf
# with open("idf.json", "w", encoding="utf-8") as f:
#     json.dump(tfidf, f, ensure_ascii=False)
idf = None
def load_tfidf():
    global idf
    with open("Static/idf.json", "r", encoding ="utf-8") as f:
        if idf is None:
            idf = json.load(f)

# Hàm này sẽ trả về vector của nguyên một câu
def sentence_embedding(sentence):
    load_model()
    load_tfidf()
    vec = np.zeros(model.vector_size)
    total = 0

    for w in sentence:
        if w in model.wv and w in idf:
            weight = idf[w]
            vec += weight*model.wv[w]
            total += weight

    if total > 0 :
        vec /= total
    return vec

#Hàm này sẽ trả về độ giống nhau của 2 vecto a,b
def similarity(a,b):
    return np.dot(a,b)/(norm(a)*norm(b))

# data = []
# with open("vntc_train.json1", encoding= "utf-8") as f:
#     for line in f:
#         tokens = json.loads(line)
#         data.append(tokens)




embed = {}


#Mở file câu hỏi
with open("Static/Question_Library.json", "r", encoding="utf-8") as f:
    file = json.load(f)

#questions là bộ câu hỏi được trích ra từ file
for question in file:
    embed[question]= sentence_embedding(Tokenization.Tokenization(question)).tolist()

#Sau bước này thì ta lưu được vector của các câu hỏi vào file embed.json
with open("Static/embed.json", "w", encoding ="utf-8") as f:
    json.dump(embed,f, ensure_ascii=False,indent=2)













