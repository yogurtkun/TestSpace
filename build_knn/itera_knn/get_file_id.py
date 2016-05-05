import json
from function_tool import save_list

#读取信息
with open('../info_list.trn','r') as file:
    read_file = file.read()

info_list = json.loads(read_file) #两级list[id,分类，文本]

text_id_list = list(map(lambda x:x[0],info_list))  #得到的文档id的list

save_list('./id_list.plk',text_id_list)