#coding=utf-8
'''
@author: zhangy
'''

from app.models import Queue
from web.constant.dscrapy_constant import DescrapyConstant


def listAll():
    return Queue.objects.filter(deleted = DescrapyConstant.QUEUE_DELETED_NO)


def addQueue(queue):
    queue.save()
    
def getById(queue_id):
    return Queue.objects.get(id = queue_id)

def queryByServerAndQueueNameAndDb(queue_name, queue_ip, queue_port, queue_db):
    kwargs = {'queue_name':queue_name, 'queue_ip': queue_ip, 'queue_port': queue_port, 'queue_db':queue_db, 'deleted': DescrapyConstant.QUEUE_DELETED_NO}
    return Queue.objects.filter(**kwargs)

def deleteQueue(queue_id):
    return Queue.objects.filter(id = queue_id).update(deleted = DescrapyConstant.QUEUE_DELETED_YES)

def findBySpiderName(spider_name):
    return Queue.objects.filter(spider_name = spider_name)

def getLastestQueue():
    return Queue.objects.latest('id')

def findByQueueName(queue_name, db):
    kwargs = {'queue_name':queue_name, 'queue_db':db, 'deleted': DescrapyConstant.QUEUE_DELETED_NO}
    return Queue.objects.filter(**kwargs)

def updateTotalSubmitById(queue_id, total_submit):
    return Queue.objects.filter(id = queue_id).update(total_submit = total_submit)






