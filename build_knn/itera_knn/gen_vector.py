'''
对训练样本和数据直接处理成向量表便于之后的读取
'''

import json
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from function_tool import save_sparse_csr,load_sparse_csr

stemmer = PorterStemmer()
filter_s = ''
for i in range(32):
    filter_s += chr(i)
for i in range(48,58):
    filter_s += chr(i)
filter_s += string.punctuation
trans_table = {ord(c): None for c in filter_s}  #去掉标点符号,数字以及前32的ascii码的转换矩阵

#还原成词根
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

#读取信息
with open('../info_list.trn','r') as file:
    read_file = file.read()

info_list = json.loads(read_file) #两级list[id,分类，文本]

text_id_list = list(map(lambda x:x[0],info_list))  #得到的文档id的list
class_id_list = list(map(lambda x:x[1],info_list))  #得到文章分类结果的list
text_list = list(map(lambda x:x[2].lower(),info_list))  #包含内容的list
text_no_punction = list(map(lambda x:x.translate(trans_table),text_list))  #文章内容去掉标点符号

tfidf_vect = TfidfVectorizer(tokenizer= my_tokenize, stop_words='english',max_df = 0.7,min_df = 4/len(class_id_list))  #tfidf转换向量矩阵

tfidf_mat = tfidf_vect.fit_transform(text_no_punction)  #tfidf vector

save_sparse_csr('traning_vector')