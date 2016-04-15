import json

#把id对author中的重名author替换掉

dict_data_path = './un_mod_mat/'

id_author_dict = {} #id对作者名字,作者名字含有重名
same_name_dict = {} #作者名对同名作者名

with open(dict_data_path+'id_author.txt','r') as file:
    read_file = file.read()
    id_author_dict = json.loads(read_file)
    ''':type : dict'''

with open(dict_data_path+'same_name.txt','r') as file:
    read_file = file.read()
    same_name_dict = json.loads(read_file)
    ''':type : dict'''

#把id对author中的author重名去掉
for id,author_list in id_author_dict.items():
    author_list_new = list(map(lambda x:same_name_dict[x] if x in same_name_dict else x,author_list))
    id_author_dict[id] = author_list_new

#把新的dict写回去
with open(dict_data_path+'id_author.txt','w') as file:
    file_json = json.dumps(id_author_dict,ensure_ascii=False)
    file.write(file_json)
