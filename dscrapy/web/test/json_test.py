# -*- encoding: utf-8 -*-
'''
Created on 2017年9月19日

@author: huawei
'''
import json
data_str = u'[{"12142523450": {"age": 20, "name": "张三"}}, {"12142523451": {"age": 20, "name": "张三"}}, {"12142523452": {"age": 20, "name": "张三"}}, {"12142523453": {"age": 20, "name": "张三"}}, {"12142523454": {"age": 20, "name": "张三"}}]'
print data_str
print type(data_str) 



def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data


data = json_loads_byteified(data_str)
print data
print type(data)

for m in data:
    for key,value in m.items():
        print str(key)
#         print str(json.dumps(value))
        print value
        print str(value)
