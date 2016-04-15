#-*-coding:utf-8-*-
import re
from compare_name import ifSameName
from compare_name import ifSameNameP

#整理出作者和他发表的论文关系，并保存他的同名

author_dict = {}

def addToDict(name,title):

    #如果作者已经在dict中，则直接加入到dict中
    if name in author_dict:
        if not title in author_dict[name][0]:
            author_dict[name][0].append(title)
        return

    if re.search('^ *$',name):
        return

    #遍历判断是不是一个旧的名字
    for key in author_dict:
        if ifSameNameP(key,name): #如果是一个已经出的名字的新的形式
            if not title in author_dict[key][0]: #如果是一篇新出现的文章，则将其加入到文章list中
                author_dict[key][0].append(title)
            if not name in author_dict[key][1]:  #如果是一个新出现的同名，则加入到同名list中
                author_dict[key][1].append(name)
            return

    #如果到达这一步表示，这表示这的却是一个全新的名字
    author_dict[name] = ([title],[])

    # if not name in author_dict:
    #     author_dict[name] = [title]
    # else:
    #     author_dict[name].append(title)

with open('./titleset.txt','r') as file:
    read_file = file.read()

#提取出文章id和作者
name_pair = re.findall('([A-Z]\d{2}-\d{4}).*?@@@@@(.*?) *\n',read_file)

dst_file = open('./paper_author.txt','w')
log_file = open('./log.txt','w')

#遍历并构建作者和他发表的文章的dict
for pair in name_pair:
    name_list = re.split('; |;',pair[1])
    for name in name_list:
        if name == '':
            continue
        addToDict(name,pair[0])
    print('Finish '+pair[0])

#把dict中的内容输出
for key,value in author_dict.items():
    dst_file.write(key+':')
    for id in value[0]:
        dst_file.write(id+';')
    dst_file.write('@@@@@')
    for samename in value[1]:
        dst_file.write(samename+';')
    dst_file.write('\n')

    if len(value[1]) != 0:
        log_file.write(key+':')
        for id in value[0]:
            log_file.write(id+';')
        log_file.write('@@@@@')
        for samename in value[1]:
            log_file.write(samename+';')
        log_file.write('\n')


dst_file.close()
log_file.close()