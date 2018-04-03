#coding=utf-8
'''

@author: zhangy
'''
import os
from web.utils import date
from web.constant.dscrapy_constant import DescrapyConstant

class EggUploader():
    def __init__(self, f, request_ip):
        self.egg = f
        self.request_ip = request_ip.replace(".", "-")
        
    def upload(self):
        try:
            baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_dir = os.path.join(baseDir, DescrapyConstant.BASE_EGG_FILES_PATH, str(date.today()));
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
            file_dir = os.path.join(file_dir, self.request_ip)
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
            file_name = os.path.join(file_dir, self.egg.name);
            fobj = open(file_name,'wb');
            for chrunk in self.egg.chunks():
                fobj.write(chrunk);
            fobj.close();
            return file_name
        except Exception as e:
            print e

