import json

'''
转换一下结果，标记为分类对文章id
'''

with open('./label_info.txt','r') as file:
    read_file = file.read()

info_dict = json.loads(read_file)
''':type : dict'''

reverse_dict = {} #  save the class vs id, format:{class:id}

for id,class_id in info_dict.items():
    if class_id not in reverse_dict:
        reverse_dict[class_id] = [id]
    else:
        reverse_dict[class_id].append(id)

with open('./reverse_label_info.txt','w') as write_file:
    write_file.write(json.dumps(reverse_dict,ensure_ascii=False))

for key in reverse_dict.keys():
    print(key+':')
    print(len(reverse_dict[key]))
