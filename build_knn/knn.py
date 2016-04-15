import json
import nltk
import string
from sklearn.externals import joblib
from build_knn.build_classifier import my_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.neighbors import KNeighborsClassifier

'''
废弃代码
'''

trans_table = {ord(c): None for c in string.punctuation}  #去掉标点符号的转换矩阵

log_file = open('./log.txt','w')

#读取信息
with open('./info_list.trn','r') as file:
    read_file = file.read()

info_list = json.loads(read_file) #两级list[id,分类，文本]

class_id_list = list(map(lambda x:x[1],info_list)) #得到文章分类结果的list
text_list = list(map(lambda x:x[2].lower(),info_list))  #包含内容的list
text_no_punction = list(map(lambda x:x.translate(trans_table),text_list))  #文章内容去掉标点符号

knn_clf = joblib.load('./knn_model.m')

tfidf_vect = TfidfVectorizer(tokenizer= my_tokenize, stop_words='english')  #tfidf转换向量矩阵

mod_data = tfidf_vect.transform([text_no_punction[1]])
result = knn_clf.predict(mod_data)
log_file.write(result)

log_file.close()