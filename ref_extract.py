import re
import os

#废弃，并没有使用
data_dir = r'./lin_txt_annotated'
write_file = r'./result.txt'
error_file = r'./error.txt'

ref_pattern = '@+(?:R|r)eferences(.*?)$'

def divide_ref(text,pre_list):
    word_list = re.split(r'\s+',text)
    ready_info =''
    temp_list = []
    word_flag = False
    spilt_flag = False
    for i in range(len(word_list)):
        item = word_list[i]
        if item == '.':
            if word_flag == True:
                spilt_flag = True
            ready_info += (item + ' ')
            continue
        if re.match(r'^[A-Z][a-z]{2,}$',item):
            word_flag = True
            if spilt_flag == True:
                pre_list.append(ready_info)
                spilt_flag = False
                ready_info = ''
        else:
            word_flag = False
            spilt_flag = False
        ready_info += (item+' ')
    pre_list.append(ready_info)

def findref(filename):
    print(filename)
    file_path = os.path.join(data_dir,filename)
    with open(file_path,'r',errors='ignore') as file:
        read_file = file.read()

    find_ref = re.compile(ref_pattern,re.S)
    ref_infos = find_ref.findall(read_file)
    if len(ref_infos) == 0:
        error_txt.write(filename+'\n')
        return []

    refer_list = []

    for ref_info in ref_infos[0].split('\n'):
        jump_flag = False
        if len(ref_info) == 0:
            continue
        divide_ref(ref_info,refer_list)
    for item in refer_list:
        print(item)





error_txt = open(error_file,'w')
black_list = []

with open('./blacklist.txt','r') as black_file:
    black_read = black_file.read()
    black_read = black_read.split('\n')
    for item in black_read:
        print(item)
        black_list.append(item)

for parent,dirnames,filenames in os.walk(data_dir):
    for filename in filenames:
        if re.match('[A-Z]\d{2}-\d{4}',filename):
            if '000' in filename:
                continue
            findref(filename)
        break

error_txt.close()
