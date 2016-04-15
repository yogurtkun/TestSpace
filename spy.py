import re
from urllib import request

paper_link = []

#查找主页中的所有子会议链接
def findlink(text,ishtml):
    if not ishtml:
        find_links = re.findall(r'<a href="(.*?)">',text)
        for find_link in find_links:
            if not 'html' in find_link:
                paper_link.append(find_link)
    else:
        find_links = re.findall(r'<a href="(.*?)" title',text)
        for find_link in find_links:
            paper_link.append(find_link)


#获取主页的HTML
url = 'http://www.aclweb.org/anthology/'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent' : user_agent}
with open('./index.txt','w') as write_file:
    try:
        req = request.Request(url,headers = headers)
        with request.urlopen(req) as f:
            html_file = f.read().decode('UTF-8')
        write_file.write(html_file)
    finally:
        print('no error')

#提取出每个年份的链接信息
pattern = '<tr> *<th title=.*?</th>(.*?)</tr>' #nned re.S

find_ref = re.compile(pattern,re.S)

pre_file = find_ref.findall(html_file)

#有些会议的命名并不是按照大写字母的方式命名的，所以需要单独的提取方式
for sentence in pre_file:
    if not 'Biomedical NLP' in sentence:
        findlink(sentence,False)
    else:
        findlink(sentence,True)
paper_link.append('C/C65')

#对于其中一部分格式比较规范的子网页提取作者和题目的函数
def title_author(text):
    #print(text)
    result_list = []
    if re.search(r'<b>.+?</b>',text):
        #print(text)
        info_list = re.findall(r'<b>(.*?)</b>.*?<i>(.*?)</i>',text)
        #print(info_list)
        for item in info_list:
            result_list.append((item[1],item[0]))
    else:
        data_part = re.findall(r'<i>(.*?)</i>$',text)
        #print(data_part)
        info_list = re.findall(r'<i>(.*?\))',data_part[0])
        for item in info_list:
            pattern_list = re.findall(r'(.*?)</i> \((.*?)\)',item)
            for cp in pattern_list:
                result_list.append((cp[0],cp[1]))

    return result_list

#对于其中一部分的网页的提取方式，L会议为主
def special_L(text,write_file):
    at_list = re.findall(r'<p><a href=.*?([A-Z]\d{2}-\d{4})</a>.*?:(.*?)$',text,re.M)
    for item in at_list:
        authors = re.findall('<b>(.*?)</b>',item[1])
        title = re.findall('<i>(.*?)</i>',item[1])
        write_file.write(item[0]+':'+title[0]+'@@@@@')
        for author in authors:
            write_file.write(author)
        write_file.write('\n')

#提取另一些网页的提取方式，Q会议为主
def special_ta(text,write_file):
    at_list = re.findall(r'<li><a href=.*?([A-Z]\d{2}-\d{4})</a>.*?:(.*?)</li>',text)
    for item in at_list:
        authors = re.findall('<author>(.*?)</author>',item[1])
        title = re.findall('<i>(.*?)</i>',item[1])
        write_file.write(item[0]+':'+title[0]+'@@@@@')
        for author in authors:
            write_file.write(author+';')
        write_file.write('\n')

#粗提取出含有相关信息的正则表达式
whole_pattern = r'^<p><a href=\"?([A-Z]\d{2}-\d{4}).pdf\"?.*?</a>(.*?)$'#need re.M

global count
count = 0
#对于逐个子网页进行提取
for item in paper_link:
    sub_url = url + item
    req = request.Request(sub_url,headers = headers)
    with request.urlopen(req) as f:
        content = f.read().decode('UTF-8')
    #print(content)
    find_whole = re.compile(whole_pattern,re.M)
    raw_text = find_whole.findall(content)
    number = re.findall('/([A-Z]\d{2})',item)
    if len(number) == 0:
        count += 1
        path = 'G' + str(count).zfill(2)
    else:
        path = number[0]
    with open('./data/'+path+'.txt','w') as index_file:
        if len(raw_text) == 0:
            if path[0] != 'L':
                special_ta(content,index_file)
            else:
                special_L(content,index_file)
        else:
            for texts in raw_text:
                pair_list = title_author(texts[1])
                if len(pair_list) == 0:
                    continue
                for pair in pair_list:
                    index_file.write(texts[0]+':'+pair[0]+'@@@@@'+pair[1]+'\n')
    print('FINISH!'+path+'.txt')





