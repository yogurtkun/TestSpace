import json
from function_tool import compare_year

'''
将文章和它引用的文章dict转化为文章和应用它的文章dict
'''

log_file = open('./log.txt','w')

reverse_id_dict = {}

with open('../un_mod_mat/new_id_ref.txt','r') as file:
    read_file = file.read()
    id_ref_dict = json.loads(read_file)
    '''
    :type id_ref_dict : dict
    '''

for paper,related_paper_dict in id_ref_dict.items():
    for related_paper, weight in related_paper_dict.items():
        if not related_paper in reverse_id_dict:
            reverse_id_dict[related_paper] = {}
        reverse_id_dict[related_paper][paper] = weight
        # except KeyError as e:
        #     log_file.write(paper+' '+related_paper+'\n')

with open('./reverse_id.txt','w') as file:
    reverse_id_dict_json = json.dumps(reverse_id_dict)
    file.write(reverse_id_dict_json)

log_file.close()