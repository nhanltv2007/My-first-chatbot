import json
import Tokenization
import faiss
import numpy as np
import sqlite3

from Word_Embedding import sentence_embedding

index = None
embed = None
file = None
def load_data():
    global  index, embed, file
    if index is None:
        index = faiss.read_index("hnsw.faiss")
        index.hnsw.efSearch = 64
    if embed is None:
        with open("Static/embed.json", "r", encoding="utf-8") as f:
            embed = json.load(f)
    if file is None:
        with open("Static/Question_Library.json", "r", encoding="utf-8") as f:
            file = json.load(f)

#Vì file embed.json thực chất là 1 dict câu hỏi : vecto, vậy nên ta trích riêng vector ra
load_data()
vectors = np.array(list(embed.values()),dtype = "float32")
questions =list(file.keys())
answers = list(file.values())

#Hàm trả lời qua câu hỏi đưa vào
def respond(question,top_k):
    load_data()
    question = Tokenization.Tokenization(question)
    question = sentence_embedding(question)
    question = np.array(question,dtype = "float32").reshape(1,-1)
    faiss.normalize_L2(question)
    D, I = index.search(question, top_k)
    result = []
    for i in range(top_k):
        result.append(
            {
                "question" : questions[I[0][i]],
                "answer" : answers[I[0][i]],
                "similarity": float(D[0][i])
            }
        )
    return result


# #Đưa các vecto vào HNSW để tính mối liên hệ giữa chúng
# faiss.normalize_L2(vectors)
# d = 200
# index = faiss.IndexHNSWFlat(d,32) # 200 là số chiều của vecto, 32 là
# index.hnsw.efConstruction = 200
# index.hnsw.efSearch = 64
# index.add(vectors)
# faiss.write_index(index, "hnsw.faiss")

# #Lưu faiss
# index = faiss.read_index("hnsw.faiss")
# index.hnsw.efSearch = 64






