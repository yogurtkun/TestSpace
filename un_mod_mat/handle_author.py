import json

with open('./reverse_author.txt','r',encoding='utf-8') as file:
    read_file = file.read()

reverse_dict = json.loads(read_file)
'''
:type reverse_dict:dict
'''

new_dict = {}
for author,sub_authors in reverse_dict.items():
    for sub_author in sub_authors:
        if not sub_author in new_dict:
            new_dict[sub_author] = {}
        if not author in new_dict[sub_author]:
            new_dict[sub_author][author] = reverse_dict[author][sub_author]

des_file = open('./new_author_author.txt','w',encoding='utf-8')

new_dict_json = json.dumps(new_dict,ensure_ascii=False)
des_file.write(new_dict_json)

des_file.close()