from function_tool import load_sparse_csr
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import os
import re
import json

def judge_cos(filename):
    file_vector = load_sparse_csr('./file_vector/'+filename)
    cos_similarity = linear_kernel(file_vector,cen_mat)
    max_cos = max(cos_similarity[0])
    if max_cos == 0:
        wrong_list.append(filename)
        return
    if max_cos <= 0.15:
        remote_list.append(filename)


cen_mat = load_sparse_csr('./cen_matrix')
remote_list = []
wrong_list = []


count = 0
pattern = re.compile('([A-Z]\d{2}-\d{4})')
data_dir = './file_vector/'
for parent,dirnames,filenames in os.walk(data_dir):
    file_num = len(filenames)
    for filename in filenames:
        count += 1
        file_name = pattern.findall(filename)
        if len(file_name) == 1 :
            judge_cos(file_name[0])
        if count % 200 == 0:
            print('Finish '+str(count/file_num))

with open('./remote_id','w',encoding='utf-8') as file:
    file_json = json.dumps(remote_list,ensure_ascii=False)
    file.write(file_json)

with open('./wrong_id','w',encoding='utf-8') as file :
    file_json = json.dumps(wrong_list,ensure_ascii=False)
    file.write(file_json)