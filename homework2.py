# -*- coding: utf-8 -*-
"""
__author__ = "Qihang_Guan"
__studentID__ = "320180939761"
__email__ = "guanqh8@lzu.edu.cn"
__version__ = "v1.0"
"""
from subprocess import Popen,PIPE
from matplotlib import pyplot as plt

ver = "v4.4"
repo = r"D:\Git\linux-stable" #  The location of my git warehouse .
cmd_tag = 'git tag -l ' + '"' + ver + '.*"'
ver_time = Popen(cmd_tag, cwd=repo, stdout=PIPE)
ver,res = ver_time.communicate()

y = ver.decode('latin').encode('utf8').decode('utf8').split("\n")

print(y)
x_time = []
for i in y:
    cmd_time = 'git log -1 --pretty=format:\"%ct\" ' + i
    time = Popen(cmd_time, cwd=repo, stdout=PIPE).communicate()
    x_time.append(x_time)
#  print(1) a small test to show the program can run to here

plt.scatter(x_time,y)
plt.title('Release order with time')
plt.xlabel('x,time')
plt.ylabel('y,release order')
plt.show()
