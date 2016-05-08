import json

with open('./label_info.txt','r',encoding='utf-8') as file:
    read_file = file.read()

label_dict = json.loads(read_file)

c_list = [[x,0] for x in range(1,11)]

for item in label_dict.items():
    c_list[item[1]-1][1] += 1

print(c_list)