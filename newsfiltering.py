#encoding=utf-8

import pandas as pd
from data_modle.rule_keys import rule
from data_modle.rule_keys import tages
from data_modle.rule_keys import keys
#数据加载
df = pd.read_csv('d:/new/20180710173001_webspider.csv', sep='|', encoding='utf-8')
#数据指定列去重
print('数据指定列去重')
df.drop_duplicates(subset='title',keep='first',inplace=True)
print('对content列进行规则匹配，返回抓取关键字')
#对content列进行规则匹配，返回抓取关键字
df['tages_rule'] = df['content'].apply(rule)
#对content列进行命名实体识别，识别出包含‘company’标签的实体，取出大于且等于2的标签实体
df['tages_rule_1'] = df['content'].apply(tages)
print('列进行过滤，只取出符合规则的文件')
###取包含关键字的句子
print('取句子')
df['jkeys'] = df['content'].apply(keys)
#对‘tages_rule'和’tages_rule‘列进行过滤，只取出符合规则的文件
df1=df[(df['tages_rule'] != None) | (df['tages_rule_1'] !=None)]

#处理文件输出
print('saving')
df1.to_csv('d:/new/new_rule0809.csv',sep='|',encoding='utf-8')





