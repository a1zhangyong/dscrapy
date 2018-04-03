#coding=utf-8
'''
@author: zhangy
'''
import requests
from web.constant.dscrapy_constant import DescrapyConstant
class DscrapyCommand():
    
    @classmethod
    def list_projects_cmd(self, host = '127.0.0.1', port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT):
        try:
            result = requests.get("http://" + host + ":" + str(port) + '/listprojects.json', timeout = 1)
            result_str = result.content
            return eval(result_str)
        except Exception as e:
            print e
    
    @classmethod
    def nodes_status_cmd(self, project, spider, host = '127.0.0.1', port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT):
        pass
    
    @classmethod
    def list_spiders_cmd(self, project, servers):
        spiders_list = []
        params = {'project':project}
        for server in servers:
            try:
                result_json = eval(requests.get("http://" + server + '/listspiders.json', params, timeout = 1).content)
                if result_json['status'] == 'ok':
                    result_json['ip'] = server.split(":")[0]
                    spiders_list.append(result_json)
            except Exception as e:
                print e
        return spiders_list
        
    @classmethod
    def spiders_versions_cmd(self, project, spider, host = '127.0.0.1', port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT):
        pass
    
    @classmethod
    def add_version_cmd(self, server = '127.0.0.1:DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT'):
        params = {'project': 'dscrapy', 'version':'12333333', 'egg':'C:\Users\zhangy\eggs\dscrapy\1501595329.egg'}
        result = requests.post("http://" + server + '/addversion.json', data = params)
        result_str = result.content
        print eval(result_str)
    
    
    @classmethod
    def list_jobs_cmd(self, project, host = '127.0.0.1', port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT):
        params = {'project':project}
        result_str = "{}"
        try:
            result = requests.get("http://" + host + ":" + str(port) + '/listjobs.json', params, timeout = 1)
            result_str = result.content
            return eval(result_str)
        except Exception as e:
            print e
    
    @classmethod
    def start_job_cmd(self, project, spider, host = '127.0.0.1', port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT):
        params = {'project':project, 'spider':spider}
        result_json = requests.post("http://" + host + ":" + str(port) + '/schedule.json', data = params)
        return eval(result_json.content)
        
    @classmethod
    def cancel_job_cmd(self, project, job_id, host = '127.0.0.1', port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT):
        params = {'project':project, 'job':job_id}
        try:
            result_json = requests.post("http://" + host + ":" + str(port) + '/cancel.json', data = params)
            return eval(result_json.content)
        except Exception as e:
            print e
    
    #删除指定版本的target
    @classmethod
    def del_spider_cmd(self, project, version, host = '127.0.0.1', port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT):
        params = {'project':project, 'version':version}
        result_json = requests.post("http://" + host + ":" + str(port) + '/delversion.json', data = params)
        return eval(result_json.content)
    
    #删除该项目下所有版本的target
    @classmethod
    def del_project_cmd(self, project, spider, host = '127.0.0.1', port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT):
        pass
    
    @classmethod
    def find_log_cmd(self, project, spider_name, job_id, host = '127.0.0.1', port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT):
        url = "http://" + host + ":" + str(port) + "/logs/" + project + "/" + spider_name + "/" + job_id + ".log"
        return requests.get(url).content
    
 
    
    
    
    
    
    
    
        
        