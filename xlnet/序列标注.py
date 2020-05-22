# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 10:40:27 2019

@author: Sunday
"""

import fool

word = ["陈云在北京"]
for i in word:
    a = fool.analysis(i)
    
    s = set([i[3]] for i in a[1][0] if i[2] =='ns')
    print(a)
    print(s)
    
    
    

