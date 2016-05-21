from function_tool import load_sparse_csr
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import os
import re

def judge_cos(filename):
    file_vector = load_sparse_csr('./file_vector/'+filename)
    cos_similarity = linear_kernel(file_vector,cen_mat)
    print(cos_similarity)


cen_mat = load_sparse_csr('./cen_matrix')
remote_list = []

pattern = re.compile('([A-Z]\d{2}-\d{4})')
data_dir = './file_vector/'
for parent,dirnames,filenames in os.walk(data_dir):
    for filename in filenames:
        file_name = pattern.findall(filename)
        if(len(file_name) == 1):
            judge_cos(file_name[0])
            break