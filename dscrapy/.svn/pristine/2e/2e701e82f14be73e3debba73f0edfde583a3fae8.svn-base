#coding=utf-8
'''
Created on 2016-12-23

@author: Administrator
'''
from scrapy.mail import MailSender as ScrapyMailSender

class MailSender():
    def __init__(self, email):
        self.mail_from = 'a1zhangyong@sina.com'
        self.mail_user = 'a1zhangyong@sina.com'
        self.mail_pass = 'abcd8931175'
        self.mail_host = 'smtp.sina.com'
        self.email = email
        self.mail_sender = ScrapyMailSender(smtphost=self.mail_host, mailfrom=self.mail_from, smtpuser=self.mail_user, smtppass=self.mail_pass)
    def send(self):
        print self.email.email_to
        print self.mail_sender.send(to = self.email.email_to, subject = self.email.subject, body = self.email.content)
        print '已发送!'

class Email(object):
    def __init__(self, email_to = ['704062024@qq.com'], subject = None, content = None):
        self.email_to = email_to
        self.subject = subject
        self.content = content
    

if __name__ == '__main__':
    email = Email(subject = '爬虫情况汇报', content = '爬虫异常!')
    mail_sender = MailSender(email)
    mail_sender.send()

