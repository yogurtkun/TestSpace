'''
对训练样本和数据直接处理成向量表便于之后的读取
'''

import json
import nltk
import string
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from function_tool import save_sparse_csr,save_list
from datetime import datetime

print(datetime.now())

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

def cal_vector(filename):
    file_id = re.findall('([A-Z]\d{2}-\d{4}).txt', filename)[0]
    file_path = os.path.join('../../lin_txt_processed', filename)
    with open(file_path, 'rb') as file:
        read_file = file.read().decode('utf-8', errors='ignore').lower()

    text_data = read_file.translate(trans_table)
    tran_text_data = tfidf_vect.transform([text_data])
    save_sparse_csr('./tf_idf_vector/'+file_id,tran_text_data)

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

save_sparse_csr('traning_vector',tfidf_mat)
save_list('./class_id.plk',class_id_list)

data_dir = '../../lin_txt_processed/'
count = 0
print('Start! '+str(datetime.now()))
for parent,dirnames,filenames in os.walk(data_dir):
    max_file = len(filenames)
    for filename in filenames:
        if re.match('[A-Z]\d{2}-\d{4}',filename):
            if '000' in filename:
                continue
            cal_vector(filename)
            count += 1
            if count % 100 == 0:
                print('Finish '+str(count/max_file))

print(datetime.now())