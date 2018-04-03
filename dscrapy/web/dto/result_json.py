#coding=utf-8
'''
@author: zhangy
'''
class ResultJson():
    STATUS_CODE_SUCCESS = 0
    STATUS_CODE_FAIL = 1
    def __init__(self, status_code = STATUS_CODE_SUCCESS, status_message = '', data = None):
        self.status_code = status_code
        self.status_message = status_message
        self.data = data
        
    def set_status_code(self, status_code):
        self.status_code = status_code
    
    def set_status_message(self, status_message):
        self.status_message = status_message
        
    def set_data(self, data):
        self.data = data