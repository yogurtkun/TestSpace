#处理子引用的模块
import json
from function_tool import compare_year

#处理自引用时候的权重问题
dict_data_path = './un_mod_mat/'

id_author_dict = {} #id对作者名字,作者名字含有重名
author_id_dict = {} #作者名对发表的论文id，这个不包含重名
paper_ref_dict = {} #文章互相引用关系,id对id
same_name_dict = {} #作者名对同名作者名

with open(dict_data_path+'id_author.txt','r') as file:
    read_file = file.read()
    id_author_dict = json.loads(read_file)
    ''':type : dict'''

with open(dict_data_path+'author_id.txt','r') as file:
    read_file = file.read()
    author_id_dict = json.loads(read_file)
    ''':type : dict'''

with open(dict_data_path+'paper_ref.txt','r') as file:
    read_file = file.read()
    paper_ref_dict = json.loads(read_file)
    ''':type : dict'''

with open(dict_data_path+'same_name.txt','r') as file:
    read_file = file.read()
    same_name_dict = json.loads(read_file)
    ''':type : dict'''

new_id_id_dict = {} #新的文章互相引用字典，格式为id:{id:weight},weight只有1和0.5
#修改关系矩阵，将自引用的修改掉
for key_id,ref_ids in paper_ref_dict.items():
    if key_id not in id_author_dict:
        continue
    #先找出自己的作者
    now_id_author = id_author_dict[key_id]
    now_set = set(now_id_author)
    #建立字典
    if not key_id in new_id_id_dict:
        new_id_id_dict[key_id] = {}
    #遍历引用了的文章
    for ref_id in ref_ids:
        if not compare_year(key_id,ref_id):
            continue
        #再找到引用论文的作者
        ref_author = id_author_dict[ref_id]
        ref_set = set(ref_author)

        mutual = now_set & ref_set
        #如果有相同作者则权重降低
        if len(mutual) > 0:
            new_id_id_dict[key_id][ref_id] = 0.5
        else:
            new_id_id_dict[key_id][ref_id] = 1

id_id_json = json.dumps(new_id_id_dict)

with open(dict_data_path+'new_id_ref.txt','w') as file:
    file.write(id_id_json)