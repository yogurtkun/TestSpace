import re
import json
from function_tool import *

'''
建立起各种应用关系，author之间的引用关系已经去掉了自引用的情况，文章之间的自应用权重调整有专有的模块
'''

#建立dict
def build_dict(id,a_list,dict):
    dict[id] = a_list
    return

#将引用关系的dict，变为被引用关系矩阵
def reverse_the_map():
    for post_author,value in author_author_dict.items():
        for pre_author,times in value.items():
            if not pre_author in reverse_author_dict:
                reverse_author_dict[pre_author] = {}
            reverse_author_dict[pre_author][post_author] = author_author_dict[post_author][pre_author]


#建立作者之间的引用关系的dict，传入的参数是作者名和他发表的paper的list
def add_author_ref(author_name,paper):

    if not paper in paper_ref_dict:
        return
    #寻找该篇文献的引用paper
    related_papers = paper_ref_dict[paper]

    remove_paper = []
    #去除掉年份不合理的引用文献，比如06年的文献引用09年的文献
    for related_paper in related_papers:
        if not compare_year(paper,related_paper):
            remove_paper.append(related_paper)

    related_papers = list(filter(lambda x:x not in remove_paper,related_papers))

    if not author_name in author_author_dict:
        author_author_dict[author_name] = {}

    #引用的作者也都是去过重名的
    for related_paper in related_papers:
        if not related_paper in id_author_dict:
            continue
        related_authors = id_author_dict[related_paper]

        #把作者名换成本名
        related_authors = list(map(lambda x:x if not x in same_name_dict else same_name_dict[x],related_authors))

        #把自引用的情况排除
        if author_name in related_authors:
            continue

        #记录引用的结果
        for related_author in related_authors:
            if not related_author in author_author_dict[author_name]:
                author_author_dict[author_name][related_author] = 1
            else:
                author_author_dict[author_name][related_author] += 1

log_file = open('./log_info.txt','w')
debug_file = open('./debug_file.txt','w')
author_dict_file = open('./author_dict_file.txt','w')

id_author_dict = {} #id对作者名字,作者名字含有重名
paper_ref_dict = {} #id对id
same_name_dict = {} #作者名对同名作者名
author_id_dict = {} #作者名对发表的论文id，这个不包含重名
author_author_dict = {} #作者和作者的引用关系 格式：key（作者名）：[[引用作者名：次数]]
reverse_author_dict = {} #作者和引用他的作者的关系 格式:key(作者名)：[[引用他的作者名：次数]]

#建立起文章id对作者名的dict
with open('./titleset.txt','r') as file:
    read_file = file.read()

title_set_string = '([A-Z]\d{2}-\d{4}):.*?@@@@@(.*?)\n'
title_set_pattern = re.compile(title_set_string)

id_author_list = title_set_pattern.findall(read_file)
for pair in id_author_list:
    name_list = re.split('; |;',pair[1])
    clean_list(name_list)
    build_dict(pair[0],name_list,id_author_dict)

#建立id互相引用的dict
with open('./map_file.txt','r') as file:
    read_file = file.read()

map_file_string = '([A-Z]\d{2}-\d{4})@@@@@(.*?)\n'
map_file_pattern = re.compile(map_file_string)

paper_ref_list = map_file_pattern.findall(read_file)
for pair in paper_ref_list:
    ref_list = re.split('; ',pair[1])
    clean_list(ref_list)
    build_dict(pair[0],ref_list,paper_ref_dict)

#建立同名dict和author对paper的dict
with open('./paper_author.txt','r') as file:
    read_file = file.read()

author_paper_string = '(.*?):(.*?)@@@@@(.*?)\n'
author_paper_pattern = re.compile(author_paper_string)

author_info_list = author_paper_pattern.findall(read_file)
for item in author_info_list:
    paper_list = item[1].split(';')
    clean_list(paper_list)
    same_list = item[2].split(';')
    clean_list(same_list)
    for pair in same_list:
        build_dict(pair,item[0],same_name_dict)
    build_dict(item[0],paper_list,author_id_dict)

# 建立起来author之间的互相引用关系
for name,papers in author_id_dict.items():
    for paper in papers:
        add_author_ref(name,paper)

# 换成引用者到被引用者的矩阵
reverse_the_map()

for key,value in reverse_author_dict.items():
    author_dict_file.write(key+'@@@@@')
    for re_author,number in value.items():
        author_dict_file.write(re_author+':'+str(number)+';')
    author_dict_file.write('\n')

log_file.write(str(paper_ref_dict))

#把dict保存成json文件
id_author_json = json.dumps(id_author_dict,ensure_ascii=False)
paper_ref_json = json.dumps(paper_ref_dict,ensure_ascii=False)
same_name_json = json.dumps(same_name_dict,ensure_ascii=False)
author_id_json = json.dumps(author_id_dict,ensure_ascii=False)
author_author_json = json.dumps(author_author_dict,ensure_ascii=False)
reverse_author_json = json.dumps(reverse_author_dict,ensure_ascii=False)

save_path = './un_mod_mat/'
with open(save_path+'id_author.txt','w') as file:
    file.write(id_author_json)
with open(save_path+'paper_ref.txt','w') as file:
    file.write(paper_ref_json)
with open(save_path+'same_name.txt','w') as file:
    file.write(same_name_json)
with open(save_path+'author_id.txt','w') as file:
    file.write(author_id_json)
with open(save_path+'author_author.txt','w') as file:
    file.write(author_author_json)
with open(save_path+'reverse_author.txt','w') as file:
    file.write(reverse_author_json)

log_file.close()
debug_file.close()
author_dict_file.close()