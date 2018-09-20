import sys
import re
import os
###目录配置文件
all_dict = {
    'news':{
        'root_path':'/d:/root_path',
        'out_fina':'/d:/out_fina',
        'mis_file':'/d:/mis_file'
    }

}
root = re.findall('code/([\s\S]+)/',os.getcwd()[0])
configs = all_dict.get(root)
