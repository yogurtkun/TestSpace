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
filter_s = ''
for i in range(32):
    filter_s += chr(i)
for i in range(48,58):
    filter_s += chr(i)
filter_s += string.punctuation
trans_table = {ord(c): None for c in filter_s}  #去掉标点符号,数字以及前32的ascii码的转换矩阵
dict_path = '../un_mod_mat/'  #常用的字典的存储路径

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
    (distance,neigh) = knn_Clf.kneighbors(tran_text_data)  #得到最近的20个邻居的相对位置,可以用这个去索引
    if not file_id in id_author_dict:
        return
    author_list = id_author_dict[file_id]
    author_set = set(author_list)
    #构成id对class_id的pattern
    near_20 = list(map(lambda x:[text_id_list[x],class_id_list[x]],neigh[0]))
    rank_list = []
    for itera in range(len(near_20)):
        score = 1
        r_paper = near_20[itera][0]
        refer_author = id_author_dict[r_paper]
        refer_author_set = set(refer_author)
        if r_paper in id_ref_dict[file_id]:
            score += 0.75
        if file_id in id_ref_dict[r_paper]:
            score += 0.75
        if len(author_set&refer_author_set) > 0:
            score += 0.75
        rank_list.append((r_paper,near_20[itera][1],score))
    count_list = [[x,0] for x in range(1,11)]
    for item in rank_list:
        count_list[item[1]-1][1] += item[2]
    count_list = sorted(count_list,key= lambda x:x[1],reverse = True)
    label_info_dict[file_id] = (count_list[0],count_list[1],count_list[2])


log_file = open('./log.txt','w')
label_info_file = open('./label_info.txt','w')
label_info_dict = {}

#读取相关字典信息
with open(dict_path+'new_id_ref.txt','r',encoding='utf-8') as file:
    read_file = file.read()
    id_ref_dict = json.loads(read_file)  #文章互相引用字典
    '''
    :type id_ref_dict:dict
    '''

with open(dict_path+'id_author.txt','r',encoding='utf-8') as file:
    read_file = file.read()
    id_author_dict = json.loads(read_file)  #文章id和他的作者
    '''
    :type id_author_dict:dict
    '''

#读取信息
with open('./info_list.trn','r') as file:
    read_file = file.read()

info_list = json.loads(read_file) #两级list[id,分类，文本]

text_id_list = list(map(lambda x:x[0],info_list))  #得到的文档id的list
class_id_list = list(map(lambda x:x[1],info_list))  #得到文章分类结果的list
text_list = list(map(lambda x:x[2].lower(),info_list))  #包含内容的list
text_no_punction = list(map(lambda x:x.translate(trans_table),text_list))  #文章内容去掉标点符号

tfidf_vect = TfidfVectorizer(tokenizer= my_tokenize, stop_words='english',max_df = 0.7,min_df = 4/len(class_id_list))  #tfidf转换向量矩阵

tfidf_mat = tfidf_vect.fit_transform(text_no_punction)  #tfidf vector
knn_Clf = NearestNeighbors(n_neighbors=20).fit(tfidf_mat)  #构造分类器

data_dir = '../lin_txt_processed/'
count = 0
print('Start!')
for parent,dirnames,filenames in os.walk(data_dir):
    max_file = len(filenames)
    for filename in filenames:
        if re.match('[A-Z]\d{2}-\d{4}',filename):
            if '000' in filename:
                continue
            give_label(filename)
            count += 1
            if count % 100 == 0:
                print('Finish '+str(count/max_file))

# vect_file = open('../prepare/vect_file.txt','w',encoding='utf-8')
# vect_words = tfidf_vect.get_feature_names()
# for word in vect_words:
#     vect_file.write(word+'\n')
# vect_file.write(str(len(vect_words))+'\n')
# vect_file.close()

label_info_json = json.dumps(label_info_dict,ensure_ascii=False)
label_info_file.write(label_info_json)

label_info_file.close()
log_file.close()