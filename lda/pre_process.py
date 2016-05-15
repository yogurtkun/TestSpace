import nltk
import string
import re
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn import preprocessing
import numpy
from nltk.stem.porter import PorterStemmer

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
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        topic_file.write("Topic #"+str(topic_idx)+":"+'\n')
        topic_file.write(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
        topic_file.write('\n')

#分词
def my_tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens,stemmer)
    return stems

def add_new_paper(filename):
    file_id = re.findall('([A-Z]\d{2}-\d{4}).txt',filename)[0]
    file_path = os.path.join(data_dir,filename)
    with open(file_path,'r',encoding='utf-8',errors='ignore') as file:
        read_file = file.read()
    text_lower = read_file.lower()  # 包含内容的list
    text_no_punction = text_lower.translate(trans_table)  # 文章内容去掉标点符号
    data_list.append(text_no_punction)
    with open('./word_bag/'+file_id+'.txt','w',encoding='utf-8') as file:
        file.write(text_no_punction)
    paper_id_list.append(file_id)


data_list = []
paper_id_list = []
data_dir = '../lin_txt_processed/'
print('Start!')
for parent,dirnames,filenames in os.walk(data_dir):
    max_file = len(filenames)
    for filename in filenames:
        if re.match('[A-Z]\d{2}-\d{4}',filename):
            if '000' in filename:
                continue
            add_new_paper(filename)
print("text generation finish")

tf_vectorizer = CountVectorizer(max_df=0.7, min_df=4,max_features=2000,stop_words='english')
tf = tf_vectorizer.fit_transform(data_list)
print("Count finish")

lda = LatentDirichletAllocation(n_topics=25, max_iter=15,learning_method='online',learning_offset=50.,random_state=0)
lda.fit(tf)
print("LDA training finish")
tf_feature_names = tf_vectorizer.get_feature_names()
topic_file = open('./data/topic.txt','w',encoding='utf-8')
print_top_words(lda, tf_feature_names, 20)
print("Get the feature names")
topic_file.close()

result = lda.transform(tf)
print("transform all the document to topic distribution")
'''
:type : numpy.ndarray
'''
result = preprocessing.normalize(result)
with open('./data/topic_dis.txt','w',encoding='utf-8') as file:
    result_lists = result.tolist()
    for item in result_lists:
        file.write(str(item)+'\n')
print("save the result into the txt")

with open('./data/topic_dis.plk','wb') as file:
    pickle.dump(result.tolist(),file)
print("save the result into the plk file")

with open('./data/file_id.plk','wb') as file:
    pickle.dump(paper_id_list,file)

