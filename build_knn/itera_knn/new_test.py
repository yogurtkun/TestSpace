from function_tool import load_sparse_csr,load_list
from scipy.sparse import csr_matrix
import json

old_mat = load_sparse_csr('./traning_vector')
old_list = load_list('./class_id.plk')
for i in range(1,11):
    print(str(i)+':'+str(old_list.count(i)))
print(old_mat.shape)

ITERA_TIME = 1
ITERA_NEW = ITERA_TIME + 1
data_path = './temp_itera/iteration_'+str(ITERA_TIME)+'/'
class_id_list = load_list(data_path+'class_id.plk')
tf_idf_mat = load_sparse_csr(data_path+'traning_vector')
file_id_list = load_list(data_path+'id_list.plk')

for i in range(1,11):
    print(str(i)+':'+str(class_id_list.count(i)))
print(tf_idf_mat.shape)


data_path = './temp_itera/iteration_'+str(ITERA_NEW)+'/'
class_id_list = load_list(data_path+'class_id.plk')
tf_idf_mat = load_sparse_csr(data_path+'traning_vector')
file_id_list = load_list(data_path+'id_list.plk')
for i in range(1,11):
    print(str(i)+':'+str(class_id_list.count(i)))
print(tf_idf_mat.shape)


with open('../label_info_v1.txt','r',encoding='utf-8') as file:
    read_file = file.read()
label_dict = json.loads(read_file)
''':type : dict'''

item = label_dict.values()
a_list = list(map(lambda x:x[0][0],item))
for i in range(1,11):
    print(str(i)+':'+str(a_list.count(i)))