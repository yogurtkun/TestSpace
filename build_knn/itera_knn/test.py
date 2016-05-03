import json
import nltk
import string
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from function_tool import save_sparse_csr,load_sparse_csr
from datetime import datetime

print(datetime.now())

stemmer = PorterStemmer()
filter_s = ''
for i in range(32):
    filter_s += chr(i)
for i in range(48,58):
    filter_s += chr(i)
filter_s += string.punctuation
trans_table = {ord(c): None for c in filter_s}  #去掉标点符号的转换矩阵

def stem_tokens(tokens,stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

#分词
def my_tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens,stemmer)
    return stems

info_list = ['Hello boys, you are good','I prefer to take some notes','The important experiences I have recently is you']
text_list = list(map(lambda x:x.lower(),info_list))  #包含内容的list
text_no_punction = list(map(lambda x:x.translate(trans_table),text_list))  #文章内容去掉标点符号

tfidf_vect = TfidfVectorizer(tokenizer= my_tokenize, stop_words='english')  #tfidf转换向量矩阵

tfidf_mat = tfidf_vect.fit_transform(text_no_punction)  #tfidf vector
print(tfidf_vect.get_feature_names())
print(tfidf_mat)

test_file = 'test'
save_sparse_csr(test_file,tfidf_mat)

t = load_sparse_csr(test_file)
print(t)

print(datetime.now())
