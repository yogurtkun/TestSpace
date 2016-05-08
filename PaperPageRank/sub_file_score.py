import json
import networkx as nx

'''
子领域的pageRank结果,just for test
'''

with open('../un_mod_mat/new_id_ref.txt','r') as file:
    read_file = file.read()
    id_ref_dict = json.loads(read_file)
    '''
    :type id_ref_dict:dict
    '''

with open('../build_knn/label_info.txt','r') as file:
    read_file = file.read()
    class_dict = json.loads(read_file)
    '''
    :type class_dict:dict
    '''

graph = nx.DiGraph()

flag = 10

for paper,refer_dict in id_ref_dict.items():
    if not paper in class_dict:
        continue
    if not class_dict[paper][0][0] == flag:
        continue
    for refer,weight in refer_dict.items():
        if not refer in class_dict:
            continue
        f_c = class_dict[refer][0]
        s_c = class_dict[refer][1]
        if f_c[1] == s_c[1]:
            continue
        if not f_c[0] == flag:
            continue
        graph.add_weighted_edges_from([(paper,refer,weight)])

sub_scores = nx.pagerank(graph)

nodes = nx.number_of_nodes(graph)
print(nodes)

sub_scores_list = []

for key,value in sub_scores.items():
    sub_scores_list.append((key,value))

sub_scores_list = sorted(sub_scores_list,key= lambda x:x[1],reverse=True)

with open('./scores_'+str(flag)+'.txt','w') as file:
    for item in sub_scores_list:
        file.write(item[0]+':'+str(item[1])+'\n')