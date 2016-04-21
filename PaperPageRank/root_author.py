import json
from function_tool import get_rank_paper_list

file_dict = {}
id_author_dict = {}

log_file = open('./log.txt','w')

with open('../un_mod_mat/id_author.txt','r',encoding='utf-8') as file:
    read_file = file.read()
    id_author_dict = json.loads(read_file)

data_path = './result/scores_'
for i in range(1,11):
    sub_path = data_path+str(i)+'.txt'
    file_dict[i] = get_rank_paper_list(sub_path)

print(file_dict[1])

for i in range(1,11):
    name_rank_dict = {}
    for j in range(0,int(len(file_dict[i])/10)):
        file_id = file_dict[i][j][0]
        file_author = id_author_dict[file_id]
        for author_i in range(len(file_author)):
            author = file_author[author_i]
            if not author in name_rank_dict:
                name_rank_dict[author] = 0
            if author_i == len(file_author)-1 or (len(file_author) > 4 and author_i >= len(file_author)-2):
                name_rank_dict[author] += file_dict[i][j][1]
            else:
                name_rank_dict[author] += file_dict[i][j][1]/2
    name_rank_dict_json = json.dumps(name_rank_dict)
    with open('./author_result/result_a_'+str(i)+'.txt','w') as file:
        file.write(name_rank_dict_json)
    break

log_file.close()