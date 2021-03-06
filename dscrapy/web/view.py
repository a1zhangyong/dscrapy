#coding=utf-8
from datetime import datetime
import sys

from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render

from app.models import Targets, Queue
from control.dscrapy_control import JobControl, TargetControl, QueueControl, TaskControl, LogControl, NodeControl, SpiderControl, MonitorControl
from web.constant.dscrapy_constant import DescrapyConstant
from web.dto.result_json import ResultJson
from web.net.remote_client import LinuxClient
from web.utils.egg_uploader import EggUploader
import json
import re
from utils import date
import random
import math
import base64
from ctypes import *

reload(sys)
sys.setdefaultencoding('utf-8')

def include(request):
    return render(request, 'include.html')
def index(request):
    context          = {}
    return render(request, 'index.html', context)

def welcome(request):
#     client_list = Redis.client_list()
    context          = {}
    context['hello'] = 'Hello World!'
#     context['client'] = client_list[0]
    return render(request, 'welcome.html', context)

def list_targets(request):
    context = {}
    tc = TargetControl()
    all_targets = tc.get_all_targets()
    context['result'] = all_targets
    return render(request, 'targets_list.html', context)

def del_target(request):
    project = request.GET['project']
    target_id = request.GET['target_id']
    version = request.GET['version']
    host_ip = request.GET['host_ip']
    is_online = request.GET['is_online']
    tc = TargetControl()
    result = tc.del_target(target_id, project, host_ip, version, DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT, is_online)  #返回删除记录条数
    tc.get_all_targets()    #重新加载配置
    return HttpResponse(result.status_message)
def to_add_target(request):
    context = {}
    return render(request, 'target_add.html', context)

#添加target
def add_target(request):
    context = {}
    host_ips = request.GET['host_ips']
    project_name = request.GET['project_name']
    targets = []
    for host_ip in host_ips.split(";"):
        target = Targets()
        target.host_ip = host_ip
        target.host_port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT
        target.project_name = project_name
        target.target_name = host_ip + "-" + project_name
        target.status = 0
        target.deleted = 0
        target.create_time = datetime.now()
        targets.append(target)
    tc = TargetControl()
    result = tc.add_targets(targets)
    context['message'] = result.status_message
    return render(request, 'target_add.html', context)

def deploy_targets(request):
    context = {}
    request_ip = '0.0.0.0'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        request_ip = request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        request_ip = request.META['REMOTE_ADDR'] 
    project_name = request.POST['project_name']
    settings = request.POST['settings']
    host_ip = request.POST['host_ip']
    project_egg_file = request.FILES.get('project_egg')
    if not project_egg_file:
        context['message'] = '文件不能为空!'
        return render(request, 'targets_list.html', context)
    project_egg_version = project_egg_file.name.split(".")[0]
    eu = EggUploader(project_egg_file, request_ip)
    file_name = eu.upload()
    if not file_name:
        context['message'] = '文件上传失败!'
        return render(request, 'targets_list.html', context)
    host_port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT
    tc = TargetControl()
    result_json = tc.deploy_targets(project_name, settings, host_ip, host_port, file_name, project_egg_version)
    tc = TargetControl()
    all_targets = tc.get_all_targets()
    context['result'] = all_targets
    update_params = []
    if result_json and len(result_json) > 0:
        server_info = ""
        for target_info in result_json:
            param = {}
            param['target_id'] = target_info['target_id']
            param['target_status'] = 1  #将爬虫状态标志为已部署
            param['latest_version'] = project_egg_version
            update_params.append(param)
            server_info += target_info['host_ip'] + "\t"
        success_message = "成功部署%s个target，分别位于(%s)服务器上" %(len(result_json), server_info)
        context['message'] = '部署成功[%s]!' %success_message
    else:
        context['message'] = '部署失败[%s]!' %result_json
    tc.update_targets_status_and_version(update_params)
    return render(request, 'targets_list.html', context)

def ajax_deploy_targets(request):
    project_name = request.GET['project_name']
    settings = request.GET['settings']
    host_ip = request.GET['host_ip']
    host_port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT
    tc = TargetControl()
    result_json = tc.deploy_targets(project_name, settings, host_ip, host_port)
    result_message = ""
    if result_json and len(result_json) > 0:
        server_info = ""
        for target_info in result_json:
            server_info += target_info['host_ip'] + "\t"
        success_message = "成功部署%s个target，分别位于(%s)服务器上" %(len(result_json), server_info)
        result_message = '部署成功[%s]!' %success_message
    else:
        result_message = '部署失败[%s]!' %result_json
    return HttpResponse(result_message)

def ajax_find_servers(request):
    project_name = request.GET['project_name']
    tc = TargetControl()
    result_json = tc.getTargetsByProjectName(project_name)
    return JsonResponse(result_json.__dict__, content_type='application/json')

def list_all_queues(request):
    context = {}
    qc = QueueControl()
    result =  qc.list_queues()
    context['result'] = result
    return render(request, 'queues_list.html', context)

def to_add_queue(request):
    context = {}
    return render(request, 'queue_add.html', context)

def add_queue(request):
    context = {}
    queue = Queue()
    queue_name = request.GET['queue_name']
    spider_name = request.GET['spider_name']
    queue_ip = request.GET['queue_ip']
    queue_db = request.GET['queue_db']
    queue_describ = request.GET['queue_describ']
    queue.queue_name = queue_name
    queue.spider_name = spider_name
    queue.queue_ip = queue_ip
    queue.queue_port = DescrapyConstant.DEFAULT_DSCRAPY_REDIS_PORT
    queue.queue_db = queue_db
    queue.total_submit = 0
    queue.queue_describ = queue_describ
    queue.create_time = datetime.now()
    queue.deleted = DescrapyConstant.QUEUE_DELETED_NO
    qc = QueueControl()
    result = qc.add_queue(queue)
    context['message'] = result.status_message
    return render(request, 'queue_add.html', context)

def del_queue(request):
    queue_id = request.GET['queue_id']
    qc = QueueControl()
    result = qc.del_queue(queue_id)
    return HttpResponse(result.status_message)

def to_add_tasks(request):
    context = {}
    queue_id = request.GET['queue_id']
    qc = QueueControl()
    queue = qc.get_queue_by_id(int(queue_id))
    context['result'] = queue
    return render(request, 'tasks_add.html', context)

#添加普通任务
def add_normal_tasks(request):
    queue_id = request.GET['queue_id']
    queue_ip = request.GET['queue_ip']
    queue_port = DescrapyConstant.DEFAULT_DSCRAPY_REDIS_PORT
    queue_name = request.GET['queue_name']
    queue_db = request.GET['queue_db']
    tasks = request.GET['tasks']
    params = {'host_ip': queue_ip, 'host_port': queue_port, 'db':queue_db, 'key':queue_name, 'tasks':tasks}
    tc = TaskControl()
    result = tc.add_normal_tasks(params)
    
    context = {}
    qc = QueueControl()
    queue = qc.get_queue_by_id(int(queue_id))
    context['result'] = queue
    context['message'] = result.status_message
    return render(request, 'tasks_add.html', context)

def ajax_add_tasks(request):
    result_json = ResultJson()
    server = request.POST.get('server')
    db = request.POST.get('db')
    queue_name = request.POST.get('queue_name')
    tasks = request.POST.getlist('tasks')
    limit = request.POST.get('limit')
    data_type = request.POST.get('data_type')
    if not data_type:
        data_type = DescrapyConstant.QUEUE_DATA_TYPE_LIST
    if not queue_name:
        result_json.set_status_code(ResultJson.STATUS_CODE_FAIL)
        result_json.set_status_message("队列名称不能为空")
        return JsonResponse(result_json.__dict__, content_type='application/json')
    if not tasks:
        result_json.set_status_code(ResultJson.STATUS_CODE_FAIL)
        result_json.set_status_message("任务不能为空")
        return JsonResponse(result_json.__dict__, content_type='application/json')
    if not server:
        server = DescrapyConstant.DEFAULT_DSCRAPY_REDIS_IP
    if not db:
        db = DescrapyConstant.DEFAULT_DSCRAPY_REDIS_DB
    if not limit:
        limit = DescrapyConstant.QUEUE_TASKS_LIMIT
    data_type = int(data_type)
    params = None
    if data_type == DescrapyConstant.QUEUE_DATA_TYPE_LIST:
        params = {"server": server, "db":db, "queue_name":queue_name, "tasks":tasks, "limit":int(limit), "data_type":data_type}
    if data_type == DescrapyConstant.QUEUE_DATA_TYPE_HASH:
        params = {"server": server, "db":db, "queue_name":queue_name, "tasks":tasks[0], "limit":int(limit), "data_type":data_type}
    tc = TaskControl()
    result = tc.submit_tasks(params)
    return JsonResponse(result.__dict__, content_type='application/json')
    

#添加带有优先级任务
def add_priority_tasks(request):
    return HttpResponse("<p>提交成功!</p>")

#删除任务
def del_tasks(request):
    tasks = request.GET['tasks']
    return HttpResponse("<p>提交成功!</p>")

#清空所给队列的所有任务
def clear_tasks(request):
    queue = request.GET['queue']
    return HttpResponse("<p>提交成功!</p>")

#克隆job, 可以动态加载settings TODO
def clone_job(request):
    spider = request.GET['spider']
    host_ip = request.GET['host_ip']
    project =request.GET['project']
    host_port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT
    params = {'project':project, 'spider':spider, 'host_ips':host_ip, 'host_port':host_port}
    jc = JobControl()
    results = jc.start_jobs(params)
    message = ''
    if results and len(results) > 0:
        result = results[0]
        if result['status'] == 'ok':
            message = '克隆成功'
        else:
            message = '克隆失败'
    return HttpResponse(message)

def to_add_job(request):
    context = {}
    sc = SpiderControl()
    projects = sc.getAllProjects()
    context['result'] = projects
    return render(request, 'job_add.html', context)

#新增job, 可以动态加载settings TODO
def add_jobs(request):
    context = {}
    project = request.GET['project_name']
    spider = request.GET['spider_name']
    host_ips = request.GET['host_ips']
    server_multi = request.GET['server_multi']
    try:
        server_multi = int(server_multi)
        if server_multi >= 50:
            server_multi = 50
    except:
        server_multi = 1
    host_port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT
    params = {'project':project, 'spider':spider, 'host_ips':host_ips, 'host_port':host_port}
    jc = JobControl()
    for i in range(0, server_multi):
        result_json = jc.start_jobs(params)
    message = ''
    if result_json and len(result_json) > 0:
        success_count = 0
        success_server = ''
        fail_count = 0
        fail_server = ''
        for target_info in result_json:
            if target_info['status'] == 'ok':
                success_count += 1
                success_server += target_info['host_ip'] + "\t"
            else:
                fail_count += 1
                fail_server += target_info['host_ip'] + "\t"
        message = "成功%s个，位于{%s}服务器上, 失败%s个, 位于{%s}服务器上" %(success_count * server_multi, success_server, fail_count, fail_server)
    else:
        message = '运行失败!'
    sc = SpiderControl()
    projects = sc.getAllProjects()
    context['result'] = projects
    context['message'] = message
    return render(request, 'job_add.html', context)


def ajax_add_job(request):
    result_json = ResultJson()
    project = request.GET['project_name']
    spider = request.GET['spider_name']
    host_ip = request.GET['host_ip']
    host_port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT
    params = {'project':project, 'spider':spider, 'host_ips':host_ip, 'host_port':host_port}
    jc = JobControl()
    result = jc.start_jobs(params)
    if result and len(result) > 0:
        status = result[0]['status']
        if status == 'ok':
            result_json.set_status_code(ResultJson.STATUS_CODE_SUCCESS)
            result_json.set_status_message("运行成功")
        else:
            result_json.set_status_code(ResultJson.STATUS_CODE_FAIL)
            result_json.set_status_message("运行失败")
    return JsonResponse(result_json.__dict__, content_type='application/json')

#取消job
def cancel_job(request):
    project = request.GET['project']
    job_id = request.GET['job_id']
    host_ip = request.GET['host_ip']
    host_port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT
    params = []
    param = {'project':project, 'job_id':job_id, 'host_ip':host_ip, 'host_port':host_port}
    params.append(param)
    jc = JobControl()
    result = jc.cancel_jobs(params)
    return HttpResponse(result.status_message)

#batch delete
def cancel_jobs(request):
    jobs = json.loads(request.body)
    host_port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT
    params = []
    for job in jobs:
        param = {'project':job['project'], 'job_id':job['job_id'], 'host_ip':job['host_ip'], 'host_port':host_port}
        params.append(param)
    jc = JobControl()
    result = jc.cancel_jobs(params)
    return HttpResponse(result.status_message)
    
#list job   
def list_jobs(request):
    context = {}
    project = request.GET['project']
    host_ip = request.GET['host_ip']
    host_port = DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT
    params = {'project':project, 'host_ip':host_ip, 'host_port':host_port}
    jc = JobControl()
    result = jc.list_jobs(params)
    context['result'] = result
    return render(request, 'jobs_list.html', context)

def list_all_jobs(request):
    context = {}
    jc = JobControl()
    result = jc.list_all_jobs()
    context['result'] = result
    return render(request, 'jobs_list.html', context)

def list_jobs_by_servers(request):
    jc = JobControl()
    spider_name = request.GET['spider_name']
    project = request.GET['project']
    host_ips = str(request.GET['host_ips'])
    params = []
    host_ip_list = host_ips.split(",")
    for host_ip in host_ip_list:
        if host_ip:
            param = {'spider_name':spider_name, 'project':project, 'host_ip':host_ip, 'host_port': DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT}
            params.append(param)
    results = jc.list_jobs_by_servers(params)
    result_str = ''
    for result in results:
        result_str += str(result) + "<br>"
    return HttpResponse(result_str)


def find_log(request):
    project = request.GET['project']
    spider_name = request.GET['spider_name']
    host = request.GET['host_ip']
    job_id = request.GET['job_id']
    lc = LogControl()
    result = lc.findLog(project, spider_name, host, DescrapyConstant.DEFAULT_DSCRAPY_SERVER_PORT, job_id)
    result = result.replace("\n", "<br>")
    return HttpResponse("<p>" + result + "</p>")

def list_nodes(request):
    context = {}
    nc = NodeControl()
    nodes = nc.getNodesList()
    context['result'] = nodes
    server = random.choice(nodes)['host_ip']
    context['server'] = server
    return render(request, 'nodes_list.html', context)

def watch_node(request):
    node_ip = request.GET['node_ip']
    user_name = request.GET['user_name']
    password = request.GET['password']
    cmd = request.GET['cmd']
    lc = LinuxClient()
    result_json = None
    if lc.connect(node_ip, user_name, password):
        if cmd == "cpu":
            result_json = lc.watch_cpu()
        if cmd == "disk":
            result_json = lc.watch_disk()
        if cmd == "memery":
            result_json = lc.watch_memery()
    else:
        result_json = ResultJson()
        result_json.set_status_code(ResultJson.STATUS_CODE_FAIL)
        result_json.set_status_message("用户名或密码错误, 连接失败!")
    return JsonResponse(result_json.__dict__, content_type='application/json')

def list_spiders(request):
    context = {}
    sc = SpiderControl()
    projects = sc.getAllProjects()
    result_json = sc.list_all_spiders(projects)
    context['result'] = result_json
    return render(request, 'spiders_list.html', context)

def to_load_line_chart(request):
    context = {}
    qc = QueueControl()
    result = qc.list_queues()
    context['result'] = result
    mc = MonitorControl()
    result_json = mc.getRecentlyQueuesMonitor()
    context['datas'] = result_json.data
    return render(request, 'line.html', context)

def ajax_load_line_chart(request):
    queue_name = request.GET['queue_name']
    search_date = int(request.GET['date'])
    if not queue_name:
        qc = QueueControl()
        queue = qc.get_lastest_queue()
        queue_name = queue.queue_name
    mc = MonitorControl()
    result_json = mc.get_monitors_by_queue_and_date(queue_name, search_date)
    return JsonResponse(result_json.__dict__, content_type='application/json')
    
def ajax_load_table(request):
    mc = MonitorControl()
    result_json = mc.getRecentlyQueuesMonitor()
    return JsonResponse(result_json.__dict__, content_type='application/json')

def ajax_load_cpu_line(request):
    server = request.GET['server']
    lc = LinuxClient()
    result_json = ResultJson()
    if lc.connect(server, DescrapyConstant.DEFAULT_NODE_USER, DescrapyConstant.DEFAULT_NODE_PASSWORD):
        times = 2
        result = lc.watch_cpu(times, False).data
        lines = result.split("\n")
        cpu_lines = []
        for line in lines:
            pattern = re.compile(r"^%Cpu.*$")
            match = pattern.search(line)
            if match:
                cpu_lines.append(match.group())
        used_rate = 100 - float(cpu_lines[times - 1].split(",")[3].strip().replace(" ", "|").split("|")[0])
        date_time = date.format_date(datetime.now())
        data = {"date": date_time, "rate": used_rate, "server": server}
        result_json.set_data(data)
        result_json.set_status_code(ResultJson.STATUS_CODE_SUCCESS)
    else:
        result_json.set_status_code(ResultJson.STATUS_CODE_FAIL)
        result_json.set_status_message("[%s]用户名或密码错误, 连接失败!" %server)
    return JsonResponse(result_json.__dict__, content_type='application/json')

def ajax_load_node(request):
    result_json = ResultJson()
    server = request.GET['server']
    lc = LinuxClient()
    data = {}
    if lc.connect(server, DescrapyConstant.DEFAULT_NODE_USER, DescrapyConstant.DEFAULT_NODE_PASSWORD):
        memery = lc.doCmd("free -m", False)
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
        data['memery_total'] = memery_total
        data['memery_used_rate'] = memery_used_rate
        disk = lc.watch_disk(False).data
        lines = disk.split("\n")
        if len(lines) > 1:
            disk_line = lines[1]
            disk_result = disk_line.replace(" ", "|")
            disk_reults = disk_result.split("|")
            results = []
            for disk in disk_reults:
                if disk:
                    if not "/" in disk:
                        results.append(disk)
            data['disk_total'] = results[0] if len(results) > 0 else "unknow"
            data['disk_used_rate'] = results[3] if len(results) > 3 else "unknow"
        cpus = lc.count_cpus().data
        data['cpus'] = cpus
        result_json.set_data(data)
        result_json.set_status_code(ResultJson.STATUS_CODE_SUCCESS)
    else:
        result_json.set_status_code(ResultJson.STATUS_CODE_FAIL)
        result_json.set_status_message("[%s]用户名或密码错误, 连接失败!" %server)
    return JsonResponse(result_json.__dict__, content_type='application/json')


def ajax_load_jobs_info(request):
    server = request.GET['server']
    nc = NodeControl()
    result_json = nc.getNodeProjectAndJobs(server)
    return JsonResponse(result_json.__dict__, content_type='application/json')

def ajax_random_get_server(request):
    result_json = ResultJson()
    nc = NodeControl()
    nodes = nc.getAllNodes()
    server = random.choice(nodes)['host_ip']
    result_json.set_data(server)
    result_json.set_status_code(ResultJson.STATUS_CODE_SUCCESS)
    return JsonResponse(result_json.__dict__, content_type='application/json')


# def iccode_crack(request):
#     result_json = ResultJson()
#     dll = windll.LoadLibrary('OCR.dll')
#     img = request.GET['img']
#     data = base64.b64decode(img)  
#     ret = dll.OCR(data, len(data))
#     ocrVal= c_char_p(ret)
#     print ocrVal.value
#     result_json.set_data(str(ocrVal.value))
#     result_json.set_status_code(ResultJson.STATUS_CODE_SUCCESS)
#     return JsonResponse(result_json.__dict__, content_type='application/json')
