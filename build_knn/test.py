import json

with open('./label_info.txt','r') as file:
    read_file = file.read()

info_dict = json.loads(read_file)
''':type : dict'''

print(len(info_dict.keys()))