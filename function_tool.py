import re

#在应用关系中，判断引用是否合理

def compare_year(id1,id2):
    year1 = re.findall('[A-Z](\d{2})-',id1)[0]
    year2 = re.findall('[A-Z](\d{2})-',id2)[0]

    year1 = int(year1)
    year2 = int(year2)

    year1 = year1 - 100 if year1 > 50 else year1
    year2 = year2 - 100 if year2 > 50 else year2

    return year1 >= year2

def clean_list(x):
    while '' in x:
        x.remove('')


def get_rank_paper_list(path):
    '''
    :param path:str
    :return :list
    '''
    with open(path,'r') as file:
        paper_lines = file.readlines()

    paper_list = list(map(lambda x:re.findall(r'([A-Z]\d{2}-\d{4}):(.*?)\n',x)[0],paper_lines))
    return_list = list(map(lambda x:(x[0],float(x[1])),paper_list))
    return return_list