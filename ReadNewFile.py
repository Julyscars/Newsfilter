# -*- coding: utf-8 -*-
"""=============================================
File name :ReadNewFile
author : Sophie
Software : PyCharm
Created on :2018/9/18 15:04
============================================="""
# code is far away from bugs with the god animal protecting
import pandas as pd
import os
import logging


class ReadFile(object):
    def __init__(self, path=None, today=None, yesday=None):
        self.today = today.replace('-', '')
        self.yesday = yesday.replace('-', '')
        self.file_path = path
        self.logger = logging.getLogger('News.ReadFile')
        try:
            self.his = pd.read_pickle('./his.pkl')
        except Exception as err:
            self.logger.error(err)
            self.his = pd.Series()

    def ReadNewFile(self):
        remote_file_ls = self.remote_file()
        new_file = self.cheak_new_file(remote_file_ls)
        success = []
        final_path = []
        date = self.today.replace('-', '')
        for fn in new_file:
            this_date = self.today if date in fn else self.yesday
            final_file = os.path.join(self.file_path, this_date, fn)
            try:
                success.append(fn)
                final_path.append(final_file)
            except Exception as err:
                self.logger.error(err)
            self.update_his_file(success)
        return final_path

    def remote_file(self):
        new_ls = os.listdir(os.path.join(self.file_path, self.today))
        new_ls.extend(os.listdir(os.path.join(self.file_path, self.yesday)))
        new_ls = {i for i in new_ls if i.endswith('.out')}
        new_ls = {i for i in new_ls if not i.endswith('specialspider.out')}
        return new_ls

    def cheak_new_file(self, remote_file_ls):
        his = set(self.his)
        new_file_ls = list(remote_file_ls.difference(his))
        new_file_ls.sort()
        return new_file_ls

    def update_his_file(self, new_file):
        his = self.his.append(pd.Series(new_file))
        his = his.sort_values()[-1000:]
        his.to_pickle('./his.pkl')


if __name__ == '__main__':
    hf = ReadFile(path='/data/yuqing_nlp/nlp_out/web', today='2018-09-18', yesday='2018-09-17')
    fl = hf.ReadNewFile()
    print(fl)
