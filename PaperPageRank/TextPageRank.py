import json
import networkx as nx

'''
做全局pagerank的代码部分
'''
with open('../un_mod_mat/new_id_ref.txt','r') as file:
    read_file = file.read()
    id_ref_dict = json.loads(read_file)

graph = nx.DiGraph()

for paper,related_paper_dict in id_ref_dict.items():
    for refer_papers,weight in related_paper_dict.items():
        graph.add_weighted_edges_from([(paper,refer_papers,weight)])

scores = nx.pagerank(graph)

scores_list = []
for key,value in scores.items():
    scores_list.append((key,value))

print(scores_list)

scores_list = sorted(scores_list,key=lambda x:x[1],reverse=True)

with open('./scores.txt','w') as file:
    for item in scores_list:
        file.write(item[0]+':'+str(item[1])+'\n')
