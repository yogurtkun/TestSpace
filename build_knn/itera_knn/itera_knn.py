'''
迭代版的KNN
'''

import json
import os
from scipy.sparse import vstack
from function_tool import *
from datetime import datetime
from sklearn.neighbors import NearestNeighbors

def add_data(filename):
    file_id = re.findall('([A-Z]\d{2}-\d{4}).npz', filename)[0]
    # 判断该文档id是否已经在训练集中
    if file_id in file_id_list:
        return
    # 加载进tf-idf向量
    file_tf_idf = load_sparse_csr('./tf_idf_vector/'+file_id)

    (distance, neigh) = knn_clf.kneighbors(file_tf_idf)  # 得到最近的20个邻居的相对位置,可以用这个去索引
    author_list = id_author_dict[file_id]  # 得到该篇文章的id
    author_set = set(author_list)  # 转换成集合
    # 构成id对class_id的pattern
    near_20 = list(map(lambda x: [file_id_list[x], class_id_list[x]], neigh[0]))
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
        if len(author_set & refer_author_set) > 0:
            score += 0.75
        rank_list.append((r_paper, near_20[itera][1], score))
    count_list = [[x, 0] for x in range(1, 11)]
    for item in rank_list:
        count_list[item[1] - 1][1] += item[2]
    count_list = sorted(count_list, key=lambda x: x[1], reverse=True)
    if count_list[0][1] - count_list[1][1] >= THRESHOLD:
        global tf_idf_mat_new
        tf_idf_mat_new = vstack([tf_idf_mat_new,file_tf_idf])
        class_id_list.append(count_list[0][0])
        file_id_list.append(file_id)
        return True
    else:
        return False



print(datetime.now())

class_id_list = load_list('./class_id.plk')
tf_idf_mat = load_sparse_csr('./traning_vector')
file_id_list = load_list('./id_list.plk')
THRESHOLD = 10
ITERA_TIME = 1
tf_idf_mat_new = tf_idf_mat.copy()

#读取相关字典信息
dict_path = '../../un_mod_mat/'
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

knn_clf = NearestNeighbors(n_neighbors=20).fit(tf_idf_mat)

data_dir = './tf_idf_vector/'
count = 0
print('Start!')
for parent,dirnames,filenames in os.walk(data_dir):
    max_file = len(filenames)
    for filename in filenames:
        if re.match('[A-Z]\d{2}-\d{4}',filename):
            if '000' in filename:
                continue
            if add_data(filename):
                break
            count += 1
            if count % 100 == 0:
                print('Finish '+str(count/max_file))

save_path = './temp_itera/'
new_path = save_path+'iteration_'+str(ITERA_TIME)+'/'
if not os.path.exists(new_path):
    os.makedirs(new_path)

save_list(new_path+'class_id.plk',class_id_list)
save_list(new_path+'id_list.plk',file_id_list)
save_sparse_csr(new_path+'traning_vector',tf_idf_mat_new)


print(datetime.now())