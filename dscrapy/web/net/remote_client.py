#coding=utf8
'''
@author: zhangy
'''
import paramiko
from web.constant.dscrapy_constant import DescrapyConstant
from web.dto.result_json import ResultJson
import re
import math

class LinuxClient():
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    def connect(self, host="127.0.0.1", user_name="", password="", port=22):
        try:
            self.ssh.connect(hostname=host, port=port, username=user_name, password=password)
            return True
        except Exception as e:
            print "连接失败, %s" %e
        return False
    
    def doCmd(self, cmd, is_close = True):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            result = stdout.read().decode()
            return result if result else stderr.read().decode()
        except Exception as e:
            print "出错啦, ", e
        finally:
            if is_close:
                self._close()
    
    def count_cpus(self, is_close = True):
        result_json = ResultJson()
        data = self.doCmd(DescrapyConstant.COUNT_CPUS, is_close)
        if data:
            result_json.set_status_code(ResultJson.STATUS_CODE_SUCCESS)
            result_json.set_data(data)
        else:
            result_json.set_status_code(ResultJson.STATUS_CODE_FAIL)
        return result_json
    
    def watch_memery(self, is_close = True):
        result_json = ResultJson()
        data = self.doCmd(DescrapyConstant.WATCH_MEMERY_CMD, is_close)
        if data:
            result_json.set_status_code(ResultJson.STATUS_CODE_SUCCESS)
            result_json.set_data(data)
        else:
            result_json.set_status_code(ResultJson.STATUS_CODE_FAIL)
        return result_json
    def watch_disk(self, is_close = True):
        result_json = ResultJson()
        data = self.doCmd(DescrapyConstant.WATCH_DISK_CMD, is_close)
        if data:
            result_json.set_status_code(ResultJson.STATUS_CODE_SUCCESS)
            result_json.set_data(data)
        else:
            result_json.set_status_code(ResultJson.STATUS_CODE_FAIL)
        return result_json
#         result_json = ResultJson()
#         result = self.doCmd(DescrapyConstant.WATCH_DISK_CMD)
#         lines = result.split("\n")
#         if len(lines) > 1:
#             disk_line = lines[1]
#             disk_result = disk_line.replace(" ", "|")
#             disk_reults = disk_result.split("|")
#             results = []
#             data = {}
#             for disk in disk_reults:
#                 if disk:
#                     if not "/" in disk:
#                         results.append(disk)
#             data['total'] = results[0] if len(results) > 0 else "unknow"
#             data['used'] = results[1] if len(results) > 1 else "unknow"
#             data['free'] = results[2] if len(results) > 2 else "unknow"
#             data['used_percent'] = results[3] if len(results) > 3 else "unknow"
#             result_json.set_status_code(ResultJson.STATUS_CODE_SUCCESS)
#             result_json.set_data(data)
#             return result_json
#         result_json.set_status_code(ResultJson.STATUS_CODE_FAIL)
#         return result_json
            
    
    def watch_cpu(self, times=2, is_close = True):
        result_json = ResultJson()
        data = self.doCmd(DescrapyConstant.WATCH_CPU_CMD %(times), is_close)
        if data:
            result_json.set_status_code(ResultJson.STATUS_CODE_SUCCESS)
            result_json.set_data(data)
        else:
            result_json.set_status_code(ResultJson.STATUS_CODE_FAIL)
        return result_json
    
    def _close(self):
        self.ssh.close()


if __name__ == "__main__":
    client = LinuxClient()
    client.connect("123.59.212.53", "huaw", "utn@360")
    memery = client.doCmd("free -m")
    print memery
    lines = memery.split("\n")
    if len(lines) > 1:
            disk_line = lines[1]
            disk_result = disk_line.replace(" ", "|")
            disk_reults = disk_result.split("|")
            results = []
            for disk in disk_reults:
                if disk:
                    if not "/" in disk:
                        results.append(disk)
                        
    memery_total = math.ceil(float(results[1])/1024)
    memery_used_rate = str((1 - round((int(results[3]) + int(results[5])) / float(results[1]), 2)) * 100) + "%"
    print memery_total, memery_used_rate
   
 





