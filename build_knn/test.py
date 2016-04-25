import json

with open('./reverse_label_info.txt','r',encoding='utf-8') as file:
    read_file = file.read()
    d = json.loads(read_file)

sum = 0
for key,value in d.items():
    print(str(key)+':'+str(len(value)))
    sum += len(value)

print(sum)