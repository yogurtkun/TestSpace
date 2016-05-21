from function_tool import load_sparse_csr,find_all_index
from sklearn.metrics.pairwise import linear_kernel
import json
import os

'''
该程序的作用是计算每一类文档与中心向量的余弦值并且降序排列并按类保存
'''

cen_mat = load_sparse_csr('./cen_matrix')
tran_mat = load_sparse_csr('./tran_matrix')

with open('../info_list.trn','r',encoding='utf-8') as file:
    info_list = json.load(file)

class_id_list = list(map(lambda x:x[1],info_list)) #得到文章分类结果的list

for i in range(1,11):
    id_indices = find_all_index(class_id_list,i)
    cen_vector = cen_mat[i-1:i]
    sub_mat = tran_mat[id_indices]
    cos_similarities = linear_kernel(cen_vector,sub_mat).flatten()
    related_file_indices = cos_similarities.argsort()[::-1]
    cos_value = cos_similarities[related_file_indices]
    new_path = './cen_result/result_'+str(i)+'/'
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    with open(new_path+'file.txt','w',encoding='utf-8') as file:
        file.write(str(related_file_indices.tolist()))
    with open(new_path+'cos.txt','w',encoding='utf-8') as file:
        file.write(str(cos_value.tolist()))
