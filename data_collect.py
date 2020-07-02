# -*- coding: utf-8 -*-

__authors__ = "Group 16"
__copyright__   = "Copyright 2020, Lanzhou University"
__license__ = "GPL v3.0"
__version__ = "1.0.1"
__maintainer__ = "Group 16"
__email__ = "bfeng18@lzu.edu.cn"
__date__ = 2020/6/24


import unicodedata
import csv
from subprocess import Popen, PIPE
import random

'''
This module collect the data and save as .csv file to make process easier
'''

class author:
    
    def __init__(self,name):
        self.name = name
        self.commit = []
        self.note = ''
        self.record = []

    def add_time(self,time):
        return self.commit.append(time)
    
    def get_times(self):
        return len(self.commit)
    
    def join_time(self):
        if len(self.commit) == 1:
            return 0
        else:
            return self.commit[-1],self.commit[0]
        
    def add_note(self,note):
        self.note = self.note + note
        return self.note
    
    def add_record(self,note):
        return self.record.append(note)
    
    def get_record(self):
        return self.record
    
    def get_note(self):
        return len(self.note)/len(self.commit)
    
class log:
    
    def __init__(self,verran):
        self.verran = verran
        self.repo = "D:\.git"
        self.author = {}

    def get_data(self):
        cmd = "git log --pretty=format:\"%an, %cd, %s\" "+self.verran
        p = Popen(cmd, cwd=self.repo, stdout=PIPE)
        name, time = p.communicate()
        name = unicodedata.normalize(u'NFKD', name.decode(encoding="utf-8", errors="ignore"))
        return name
    
    def get_auti(self):
        auth = []
        time = []
        note = []
        for i in self.get_data().split("\n"):
            pc = 0
            for j in i.split(","):
                if pc == 0:
                    auth.append(j)
                    pc += 1
                elif pc == 1:
                    time.append(j)
                    pc += 1
                else:
                    note.append(j)
        return auth,time,note  
    
    def complete_author(self):
        auth,time,note = self.get_auti()
        for i in range(0,len(auth)):
            if auth[i] in self.author.keys():
                self.author[auth[i]].append(time[i])
            else:
                self.author[auth[i]] = [time[i]]
        for i in range(0,len(auth)):
            if auth[i] in self.author.keys():
                self.author[auth[i]].append(note[i])
            else:
                self.author[auth[i]] = [note[i]]
        return self.author

def dict2class(d={}):
    au = []
    for i in d.keys():
        pc = 0
        new = author(i)
        for j in d[i]:
            if pc < len(d[i])/2:
                new.add_time(j)
                pc += 1
            else:
                new.add_note(j)
                new.add_record(j)
        new.get_times()
        new.join_time()
        new.get_note()
        new.get_record()
        au.append(new)
    return au

def main():
    b = log("v3.0..v5.5").complete_author()
    au = dict2class(b)
    a = random.sample(au, 2000)
    info = []
    with open("result.csv",'w',encoding='utf-8',newline="") as csvfile:
        spamwriter=csv.writer(csvfile, dialect='excel')
        spamwriter.writerow(["author","times","develop_time","notes","records"])
        for i in a:
            info = [i.name, i.get_times(), i.join_time(), i.get_note(), i.get_record()]
            spamwriter.writerow(info)


if __name__ == "__main__":
    main()
        
        
        
        

