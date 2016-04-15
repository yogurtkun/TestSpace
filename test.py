import json

log_file = open('./log.txt','w')
#读取信息
with open('./info_list.trn','r') as file:
    read_file = file.read()

info_list = json.loads(read_file) #两级list[id,分类，文本]

count = 0
for item in info_list:
    log_file.write(item[2]+'\n')
    count += 1
    if count == 2:
        break


log_file.close()