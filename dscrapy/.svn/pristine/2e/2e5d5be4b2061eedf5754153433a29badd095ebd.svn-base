#coding=utf-8
'''
@author: zhangy
'''
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet

from app.models import Targets


def listAll():
    return Targets.objects.filter(deleted = 0)

def getAllNodesByProjectName():
    return Targets.objects.filter(deleted = 0).values('host_ip', 'project_name', 'host_port').annotate(count=Count('host_ip'))
#     query = Targets.objects.filter(deleted = 0).query 
#     query.group_by = ['host_ip', 'project_name'] 
#     return QuerySet(query = query, model = Targets)

def getAllNodes():
    return Targets.objects.filter(deleted = 0).values('host_ip', 'host_port').annotate(count=Count('host_ip'))
#     query = Targets.objects.filter(deleted = 0).query 
#     query.group_by = ['host_ip'] 
#     return QuerySet(query = query, model = Targets)

def getAllProjects():
    kwargs = {'deleted': 0, 'status': 1}
    return Targets.objects.filter(**kwargs).values('project_name').annotate(count=Count('project_name'))

def getServersByProjectName(projectName):
    kwargs = {'project_name':projectName, 'deleted': 0, 'status': 1}
    return Targets.objects.filter(**kwargs).values('project_name', 'host_ip', 'host_port').annotate(count=Count('host_ip'))

def addTarget(target):
    target.save()
    
def getTargetsByProjectName(projectName):
    kwargs = {'project_name':projectName, 'deleted': 0}
    return Targets.objects.filter(**kwargs)

def getDeployedTargetsByProjectName(projectName):
    kwargs = {'project_name':projectName, 'status':1, 'deleted': 0}
    return Targets.objects.filter(**kwargs)

def getTargetsByProjectNameAndServer(projectName, server_ip, server_port):
    kwargs = {'project_name':projectName, 'host_ip': server_ip, 'host_port': server_port, 'deleted': 0}
    return Targets.objects.filter(**kwargs)

def delTarget(target_id):
    return Targets.objects.filter(id = target_id).update(deleted = 1)

def updateTargetStatusAndVersion(target_id, status, latest_version):
    return Targets.objects.filter(id = target_id).update(status = status, latest_version = latest_version)

def updateTargetIsOnline(target_id, is_online):
    return Targets.objects.filter(id = target_id).update(is_online = is_online)









