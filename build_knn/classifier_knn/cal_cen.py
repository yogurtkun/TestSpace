import os
import re
from function_tool import load_sparse_csr,save_sparse_csr
from sklearn import preprocessing

'''
该部分将所有涉及到的向量归一化,并且存储
'''

tran_mat = load_sparse_csr('../itera_knn/traning_vector')
norm_tran_mat = preprocessing.normalize(tran_mat)

save_sparse_csr('./tran_matrix',norm_tran_mat)

id_pattern = re.compile('([A-Z]\d{2}-\d{4})')
data_dir = '../itera_knn/tf_idf_vector/'
for parent,dirnames,filenames in os.walk(data_dir):
    for filename in filenames:
        file_id = id_pattern.findall(filename)[0]
        print(file_id)
        file_vector = load_sparse_csr(data_dir+file_id)
        norm_file_vector = preprocessing.normalize(file_vector)
        save_sparse_csr('./file_vector/'+file_id,norm_file_vector)