import os
import json
import shutil

pos_set = (2,4,6,7,9)

# def in_set(file_id):
#     for key,value in class_id_dict.items():
#         if file_id in value:
#             return True
#     return False

def in_set(file_id):
    if file_id not in label_dict:
        return False

    file_class = label_dict[file_id]
    if file_class[0][1] == file_class[1][1]:
        return False
    elif file_class[0][0] in pos_set:
        return True
    else:
        return False


with open('../build_knn/label_info.txt','r',encoding='utf-8') as file:
    read_file = file.read()
    label_dict = json.loads(read_file)
    '''
    :type label_dict:dict
    '''

with open('../un_mod_mat/id_author.txt','r',encoding='utf-8') as file:
    read_file = file.read()
    id_author_dict = json.loads(read_file)
    '''
    :type id_author_dict:dict
    '''

# with open('./class_file.txt','r',encoding='utf-8') as file:
#     read_file = file.read()
#     class_id_dict = json.loads(read_file)
    '''
    :type class_id_dict:dict
    '''

with open('../un_mod_mat/new_id_ref.txt','r',encoding='utf-8') as file:
    read_file = file.read()
    id_ref_dict = json.loads(read_file)
    '''
    :type id_ref_dict
    '''

class_info_file = open('./class_info.txt','w',encoding='utf-8')
sub_set_dict = {}
src_path = '../lin_txt_processed/'
des_path = './lin_txt/'

for id,sub_classes in label_dict.items():
    first_c = tuple(sub_classes[0])
    sec_c = tuple(sub_classes[1])
    thd_c = tuple(sub_classes[2])
    if first_c[1] == sec_c[1]:
        continue
    #如果是五个类中的文件
    if first_c[0] in pos_set:
        shutil.copyfile(src_path+id+'.txt',des_path+id+'.txt')
        class_info_file.write(id+'.txt'+'\n')
        class_info_file.write(str(first_c[0])+':'+str(first_c[1])+' ')
        if not first_c[0] in sub_set_dict:
            sub_set_dict[first_c[0]] = []
        else:
            sub_set_dict[first_c[0]].append(id)
    else:
        continue
    if sec_c[0] in pos_set:
        class_info_file.write(str(sec_c[0])+':'+str(sec_c[1])+' ')
    if thd_c[0] in pos_set:
        class_info_file.write(str(thd_c[0])+':'+str(thd_c[1])+' ')
    class_info_file.write('\n')
    author_list = id_author_dict[id]
    class_info_file.write(', '.join(author_list))
    class_info_file.write('\n')
    ref_paper = list(id_ref_dict[id].keys())
    ref_paper = list(filter(in_set,ref_paper))
    class_info_file.write(', '.join(ref_paper))
    class_info_file.write('\n')

with open('./class_id.txt','w',encoding='utf-8') as file:
    sub_set_dict_json = json.dumps(sub_set_dict)
    file.write(sub_set_dict_json)

class_info_file.close()