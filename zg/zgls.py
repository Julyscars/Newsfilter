# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pickle
from zhtools.langconv import * 
def cht_to_chs(line):
     line = Converter('zh-hans').convert(line)
     line.encode('utf-8')
     return line
 
 # 转换简体到繁体
def chs_to_cht(line):
     line = Converter('zh-hant').convert(line)
     line.encode('utf-8')
     return line

file = open('e:/zg/bihua.txt','r',encoding='utf-8')
dict_temp = {}
# 遍历文本文件的每一行，strip可以移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
print(file)
for line in file.readlines():
    line = line.strip()
    print(line)  
    k = line.split(' ')[0]
    v = line.split(' ')[1]
    for j in v:    
        dict_temp[j] = k 
    
print(dict_temp)        
with open('e:/zg/215.pkl', 'wb') as f:
    pickle.dump(dict_temp,f)
    
# 依旧是关闭文件

#loading zgls

#with open('e:/zg/215.pkl', 'rb') as f:
#  zgls = pickle.load(f)

 # 转换繁体到简体

#  可以打印出来瞅瞅
 

    
    
    
