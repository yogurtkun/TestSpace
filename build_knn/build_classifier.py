import json
import nltk
import string
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.neighbors import KNeighborsClassifier

'''
建立knn分类器，并对每个文档进行分类
'''

stemmer = PorterStemmer()
trans_table = {ord(c): None for c in string.punctuation}  #去掉标点符号的转换矩阵

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
    predict_label = knnClf.predict(tran_text_data)
    label_info_dict[file_id] = str(predict_label[0])

log_file = open('./log.txt','w')
tfidf_vect = TfidfVectorizer(tokenizer= my_tokenize, stop_words='english',max_df = 0.5)  #tfidf转换向量矩阵
#label_info_file = open('./label_info.txt','w')
label_info_file = open('./label_sum.txt','w')
label_info_dict = {}

#读取信息
with open('./info_list.trn','r') as file:
    read_file = file.read()

info_list = json.loads(read_file) #两级list[id,分类，文本]

class_id_list = list(map(lambda x:x[1],info_list)) #得到文章分类结果的list
text_list = list(map(lambda x:x[2].lower(),info_list))  #包含内容的list
text_no_punction = list(map(lambda x:x.translate(trans_table),text_list))  #文章内容去掉标点符号

tfidf_mat = tfidf_vect.fit_transform(text_no_punction)  #tfidf vector
knnClf = KNeighborsClassifier(n_neighbors=20)
knnClf.fit(tfidf_mat,class_id_list)  #training the classifier
#joblib.dump(knnClf,'./knn_model.m')

# data_dir = '../lin_txt_processed/'

# for parent,dirnames,filenames in os.walk(data_dir):
#     for filename in filenames:
#         if re.match('[A-Z]\d{2}-\d{4}',filename):
#             if '000' in filename:
#                 continue
#             give_label(filename)

the_result = knnClf.predict(tfidf_mat)
record_dict = {}
for itera in range(len(the_result)):
    if str(class_id_list[itera]) not in record_dict:
        record_dict[str(class_id_list[itera])] = {}
    if str(the_result[itera]) not in record_dict[str(class_id_list[itera])]:
        record_dict[str(class_id_list[itera])][str(the_result[itera])] = 0;
    else:
        record_dict[str(class_id_list[itera])][str(the_result[itera])] += 1;



#log_file.write(str(label_info_dict))
label_info_json = json.dumps(record_dict,ensure_ascii=False)
label_info_file.write(label_info_json)

label_info_file.close()
log_file.close()