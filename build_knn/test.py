import json

with open('./label_sum.txt','r') as file:
    read_file = file.read()
    l_dict = json.loads(read_file)

for m_c, s_cs in l_dict.items():
    sum = 0
    for s_c,v in s_cs.items():
        sum += v
    for s_c,v in s_cs.items():
        s_cs[s_c] = v/sum

with open('./mix_set.txt','w') as write_file:
    for key,value in l_dict.items():
        write_file.write(key+":"+'\n')
        write_file.write(str(value)+'\n')