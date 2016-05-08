import json
from function_tool import get_rank_paper_list

'''
该代码通过每个pagerank选出的每个领域的文章，按给作者打分
前几个作者只能得到该文章pagerank三分之一的分数，最后一个作者，或者（五个作者以上）的时候后两个作者会得到所有的分数，只取前10%的文章
'''

file_dict = {}
id_author_dict = {}

log_file = open('./log.txt','w')

#打开id对author的dict
with open('../un_mod_mat/id_author.txt','r',encoding='utf-8') as file:
    read_file = file.read()
    id_author_dict = json.loads(read_file)

#保存结果文件的路径
data_path = './result/scores_'
#得到pagerank每个子领域的结果
for i in range(1,11):
    sub_path = data_path+str(i)+'.txt'
    file_dict[i] = get_rank_paper_list(sub_path)

#对每个子领域的结果处理
for i in range(1,11):
    name_rank_dict = {}
    #取前百分之十的文章
    for j in range(0,int(len(file_dict[i])/10) if int(len(file_dict[i])/10) > 100 else 100):
        file_id = file_dict[i][j][0]
        #得到该文章的作者列表
        file_author = id_author_dict[file_id]
        #对每一个作者加上对应的分数
        for author_i in range(len(file_author)):
            author = file_author[author_i]
            if not author in name_rank_dict:
                name_rank_dict[author] = [0,0]
            if author_i == len(file_author)-1 or (len(file_author) > 4 and author_i >= len(file_author)-2):
                name_rank_dict[author][0] += file_dict[i][j][1]
                name_rank_dict[author][1] += 1
            else:
                name_rank_dict[author][0] += file_dict[i][j][1]
                name_rank_dict[author][1] += 1
    #排序
    name_rank_list = []
    for author,scores in name_rank_dict.items():
        name_rank_list.append((author,scores[0],scores[1]))
    name_rank_list = sorted(name_rank_list,key=lambda x:x[1],reverse=True)
    with open('./author_result/result_a_'+str(i)+'.txt','w',encoding='utf-8') as file:
        for item in name_rank_list:
            file.write(item[0]+','+str(item[2])+':'+str(item[1])+'\n')


log_file.close()