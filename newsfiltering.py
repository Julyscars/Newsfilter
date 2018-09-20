#encoding=utf-8
#加载库
import pandas as pd
from data_modle.rule_keys import rule
from data_modle.rule_keys import tages
from data_modle.rule_keys import keys
from data_modle.ReadNewFile import ReadFile
from data_modle.config import configs
import sys

import os
from logger import logger
import datetime
import logging
import shutil
import time
#获取当前目录
_get_abs_path = lambda path: os.path.normpath(os.path.join(os.getcwd()),path))
logger(logname=os.path.join(_get_abs_path(''), 'log', 'log.txt'), loglevel =1,logger = 'main')
Logger = logging.getLogger('main')
#数据加载
def read_file(file_path):

    tmp = []
    with open(file_path,'r',encoding='utf-8',errors= 'ignore') as f:
        for line in f:
            try:
                tmp.append(line.replace('\n','').split('|')[:-1])
            except:
                continue
    dfx = pd.DataFrame.from_records(tmp,columns= ['a','c','b'])
    return dfx
if __name__ =='__main__' :
    logger.infor('start int program')
    start_day = '{}'.format(datetime.date.today())
    root_path = configs['root_path']
    out_path = configs['out_fina']
    mis_file = configs['mis_file']
    while True:
        to_day = '{}'.format(datetime.date.today())
        yes_day = '{}'.format((datetime.date.today() - datetime.timedelta(days=1)))
        hfs = ReadFile(path =root_path,today=to_day,yesday=yes_day)
        file_ls = hfs.ReadNewFile()
        tmp_day = to_day.replace('-','')
        if start_day != to_day or os.path.exists('exit.text'):
            logger.infor('save hash index ...')
            sys.exit(0)
        for x ,one_file in enumerate(file_ls):
            this_date = to_day if tmp_day in one_file else yes_day
            logger.infor('reading file: {0}/{1}, {2}...'.format(x,len(file_ls),one_file))
            try:
                df = read_file(one_file)
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
            except Exception as err:
                shutil.copy(one_file,mis_file)
        if len(file_ls) <=0:
            logger.info('now not new file ending...')
            time.sleep(60)
