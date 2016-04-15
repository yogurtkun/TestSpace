#将workshop中的信息提取文章id，类别，内容处理成list，保存成json便于处理
import json
import re

data_path = '../acl_workshop/acl_workshop_filtered_hyphen_split.txt'
log_file = open('./log.txt', 'w')  # 调试文件
list_json_file = open('./info_list.trn', 'w')

text_dict = {}

with open(data_path, 'r') as file:
    read_file = file.read()

string_p = r'\d{1,4} ([A-Z]\d{2}-\d{4}) (\d{2}) [FS]\n'  # 提取信息
pattern = re.compile(string_p, re.S)

info_list = pattern.split(read_file)
new_info_list = []  # 存储新的信息的list，格式：[文档id，类别，内容]
info_list.remove('')
count = 0
sub_list = []  # new_info_list中的每个元素的单位
for item in info_list:
    if count == 0:
        sub_list = []
    if count == 1:
        sub_list.append(int(item))
    else:
        sub_list.append(item)
    count += 1
    if count == 3:
        count = 0
        new_info_list.append(sub_list)

info_json = json.dumps(new_info_list)
list_json_file.write(info_json)

log_file.close()
list_json_file.close()
