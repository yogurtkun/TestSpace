import numpy as np
from function_tool import load_sparse_csr,save_sparse_csr
import json
from scipy.sparse import vstack
from sklearn.preprocessing import normalize

'''
计算各类向量的中心
'''

tran_npz = load_sparse_csr('./tran_matrix')
with open('../info_list.trn','r',encoding='utf-8') as file:
    info_list = json.load(file)

class_id_list = list(map(lambda x:x[1],info_list)) #得到文章分类结果的list

cen_vector_dict = {}

for i in range(len(class_id_list)):
    file_class = class_id_list[i]
    if not file_class in cen_vector_dict:
        cen_vector_dict[file_class] = tran_npz[i]
    else:
        cen_vector_dict[file_class] += tran_npz[i]

temp_list = []
for id,vec in cen_vector_dict.items():
    temp_list.append((id,vec))

temp_list.sort(key=lambda x:x[0])

cen_mat = list(map(lambda x:x[1],temp_list))
res_mat = vstack(cen_mat)

norm_res_mat = normalize(res_mat)

save_sparse_csr('./cen_matrix',norm_res_mat)

