import json
import nltk
import string
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.neighbors import NearestNeighbors
import numpy as np
import scipy.spatial.distance as dis

'''
建立新版本的KNN分类器,加入迭代和变化权值等几个功能
'''

stemmer = PorterStemmer()
trans_table = {ord(c): None for c in string.punctuation}  #去掉标点符号的转换矩阵
dict_path = '../un_mod_mat/'

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

def give_label(filename):
    file_id = re.findall('([A-Z]\d{2}-\d{4}).txt',filename)[0]
    file_path = os.path.join('../lin_txt_processed',filename)
    with open(file_path,'rb') as file:
        read_file = file.read().decode('utf-8',errors='ignore').lower()

    text_data = read_file.translate(trans_table)
    tran_text_data = tfidf_vect.transform([text_data])
    (distance,neigh) = knn_Clf.kneighbors(tran_text_data)
    near_20 = neigh[0]
    #predict_label = knnClf.predict(tran_text_data)
    #log_file.write(file_id + ' ' + str(predict_label[0])+'\n')
    #label_info_dict[file_id] = str(predict_label[0])

log_file = open('./log.txt','w')
tfidf_vect = TfidfVectorizer(tokenizer= my_tokenize, stop_words='english',max_df = 0.5)  #tfidf转换向量矩阵
label_info_file = open('./label_info.txt','w')
label_info_dict = {}

#读取信息
with open('./info_list.trn','r') as file:
    read_file = file.read()

info_list = json.loads(read_file) #两级list[id,分类，文本]

text_id_list = list(map(lambda x:x[0],info_list))  #得到的文档id的list
class_id_list = list(map(lambda x:x[1],info_list))  #得到文章分类结果的list
text_list = list(map(lambda x:x[2].lower(),info_list))  #包含内容的list
text_no_punction = list(map(lambda x:x.translate(trans_table),text_list))  #文章内容去掉标点符号

tfidf_mat = tfidf_vect.fit_transform(text_no_punction)  #tfidf vector
knn_Clf = NearestNeighbors(n_neighbors=20).fit(tfidf_mat)  #构造分类器

'''
修改到这里
'''

data_dir = '../lin_txt_processed/'
# count = 0
for parent,dirnames,filenames in os.walk(data_dir):
    for filename in filenames:
        if re.match('[A-Z]\d{2}-\d{4}',filename):
            if '000' in filename:
                continue
            give_label(filename)
            break


label_info_json = json.dumps(label_info_dict,ensure_ascii=False)
label_info_file.write(label_info_json)

label_info_file.close()
log_file.close()