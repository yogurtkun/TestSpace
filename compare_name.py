#-*-coding:utf-8-*-

'''
比较两个名字是否是一个名字，主要使用的是ifSameNameP这个函数
'''

import re

s1 = 'C. H. Lee'
s2 = 'C.-H. Lee'

'''
Jong Wan Kim:W03-1116;M92-1040;M92-1023;L06-1344;W03-1116;Y15-2037;@@@@@J. Kim;Jong Myoung Kim;
Ka-Ho Wong:W15-5115;W00-1220;L06-1040;W00-1220;W15-5115;W02-1810;W00-1220;W02-1810;W02-1810;@@@@@K.F. Wong;K. Wong.;
the Annotation Group:M98-1009;X96-1028;@@@@@the PLUM Research Group;
Jiun-Da Chen:O07-2007;W96-0305;W96-0305;@@@@@J.N. Chen;
Chong Min Lee:L08-1162;W15-0605;W09-2422;N10-3008;W09-2422;W09-2422;W09-2422;H90-1062;H90-1061;P06-1095;W14-1816;@@@@@C.-H. Lee;C. H. Lee;
'''

def ifSameName(text1,text2):

    s1_list = re.split('[ -\.]',text1)
    s2_list = re.split('[ -\.]',text2)

    while '' in s1_list:
        s1_list.remove('')
    while '' in s2_list:
        s2_list.remove('')

    # try:
    if s1_list[-1] != s2_list[-1] or s1_list[0][0] != s2_list[0][0]:
        return False
    # except:
    #     print(s1_list)
    #     print(s2_list)
    #     print('@@@@@@@@@@@@@@@@@')

    set_s1 = set(s1_list[0:-1])
    set_s2 = set(s2_list[0:-1])

    print(set_s1)
    print(set_s2)

    if len(set_s1) < len(set_s2):
        short_set = set_s1
        long_set = set_s2
    else:
        short_set = set_s2
        long_set = set_s1

    mutual = set_s1&set_s2

    short_set = short_set - mutual
    long_set = long_set - mutual

    for word in short_set:
        if len(word) == 1:
            try:
                new_set = set(x[0] for x in long_set)
            except:
                print(long_set)
                print(short_set)
                print('@@@@@')
            if word in new_set:
                continue
            else:
                return False
        else:
            if word[0] in long_set:
                continue
            else:
                return False

    return True

def ifSameNameP(text1,text2):

    #把两个名字分开成一个一个单词
    s1_list = re.split('[ -\.]',text1.lower())
    s2_list = re.split('[ -\.]',text2.lower())

    #去掉空字符串
    while '' in s1_list:
        s1_list.remove('')
    while '' in s2_list:
        s2_list.remove('')

    # try:
    #如果名不一样，则视为不一样
    if s1_list[-1] != s2_list[-1]:
        return False

    #分成长名字和短名字
    if len(s1_list) < len(s2_list):
        short_name = s1_list
        long_name = s2_list
    else:
        short_name = s2_list
        long_name = s1_list

    # print(short_name)
    # print(long_name)

    #如果短名字或者长名字有一个是单个字母，那么只要判断是不是相同即可
    if len(short_name[0]) == 1 or len(long_name[0]) == 1:
        if not short_name[0][0] == long_name[0][0]:
            return False
    else:  #如果都不是缩写，则需要完全一致
        if not short_name == long_name:
            return False

    if len(short_name) <= 2:
        return True

    #取出中间部分进行对比
    new_short = short_name[1:-1]
    new_long = long_name[1:-1]

    # print(new_short)
    # print(new_long)

    #取出长名字的首字母
    C_long = list(map(lambda x:x[0],new_long))

    #print(C_long)

    #根据短名字逐次到长名字中去比较
    for word in new_short:
        if len(word) > 1:
            if not ((word in new_long) or (word[0] in new_long)):
                return False
            else:
                continue
        else:
            if not word in C_long:
                return False
            else:
                continue

    return True

print(ifSameNameP(s1,s2))