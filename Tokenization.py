import string
import re
from pyvi import ViTokenizer
def Tokenization(sentence):
    sentence = re.sub(r'[^\w\s]', ' ', sentence)
    sentence = sentence.lower()
    sentence = re.sub(r'\b\d+\b', 'NUM', sentence)
    sentence = ViTokenizer.tokenize(sentence)
    return sentence.split()

# sentence = input("Nhập câu bất kỳ:")
# print(Tokenization(sentence))
