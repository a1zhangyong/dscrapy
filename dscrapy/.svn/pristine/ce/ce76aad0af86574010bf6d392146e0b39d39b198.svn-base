#coding=utf-8
'''

@author: zhangy
'''
import socket
class ConnectCheck():
    @classmethod
    def check_remote_port(self, host, port, timeout = 2):
        result = False
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(timeout)
        try:
            sk.connect((host, int(port)))
            result = True
        except Exception:
            print 'failed connect!'
        sk.close()
        return result
    
#print ConnectCheck.check_remote_port("123.59.116.133", 6800)