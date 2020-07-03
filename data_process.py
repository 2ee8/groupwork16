#-*- coding: UTF-8 -*-
__author__ = "Group 16"
__copyright__   = "Copyright 2020, Lanzhou University"
__license__ = "GPL v3.0"
__version__ = "1.0.1"
__maintainer__ = "Group 16"
__Email__ = "bfeng18@lzu.edu.cn"
__date__ = "2020/6/20"

import git, csv,
from datetime import datetime

'''
This module use the .csv made by data_collect.py. Output the possibility of developer have
fixes and transform the timestamp in .csv file to a number represent
the period of starting to join develop the kernel.
'''

class Process():
    
    def __init__(self, dataset):
        self.dataset = dataset
        
    def get_date(self):
        """
        This function make the timestamp to the period of developer after first committing
        The result is stored in a csv file
        :param self:
        """
        file = open(self.dataset)
        fileReader = csv.reader(file)
        filedata = list(fileReader)


        for i in range(1,len(filedata)):
            data = []
            if filedata[i][2]=='0':
                filedata[i].append('0')
                continue
            a=eval(filedata[i][2])[0].split()
            if len(a) == 6:
                a = ' '.join(a)
                atime = datetime.strptime(a,"%a %b %d %H:%M:%S %Y %z")
            else:
                filedata[i].append('0')
                continue
            b=eval(filedata[i][2])[1].split()
            if len(b) == 6:
                b = ' '.join(b)
                btime = datetime.strptime(b,"%a %b %d %H:%M:%S %Y %z")
            else:
                filedata[i].append('0')
            continue
            len_s = (btime - atime).total_seconds()
            m, s = divmod(len_s, 60)
            filedata[i].append(m)
        
        with open("result_join_time.csv",'w',newline='') as t:
            writer=csv.writer(t)
            writer.writerows(filedata)

    def check_commit(self):
        """
        This function is used to calculate the frequency of fix tag in all commit of a committer.
        The result is stored in a csv file
        :param self:
        """
        csv.field_size_limit(500 * 1024 * 1024)
        with open(dataset, "r", encoding="utf-8") as f:
            data = []
            f_csv = csv.reader(f)
            for row in f_csv:
                data_son = []
                com = row[4]
                com_dic = dict([(i, com.split().count(i)) for i in com.split()])
                list = [com_dic.get('fix',0),com_dic.get('Fix', 0),com_dic.get('Fixes', 0),com_dic.get('fixes', 0)]
                average = sum(list)/int(row[1])
                data_son.append(row[0])
                data_son.append(average)
                data.append(data_son)

        with open('result_fixes.csv','w', encoding="utf-8", newline="")as d:
            header = ["authors", "fixes"]
            d_csv = csv.writer(d)
            d_csv.writerow(header)
            d_csv.writerows(data)

if __name__ == '__main__':
    a = Process("result.csv")
    a.get_date()
    a.check_commit()

