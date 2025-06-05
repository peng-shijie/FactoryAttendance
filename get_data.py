import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime
import json


url = 'https://www.yunzhijia.com/gateway/oauth2/token/getAccessToken'

url_2 = 'https://www.yunzhijia.com/gateway/workflow/form/thirdpart/findFlows?accessToken={}' # 流程列表list
# url_2.format(team_response.json()['data']['accessToken'])

url_3 = 'https://www.yunzhijia.com/gateway/workflow/form/thirdpart/viewFormInst?accessToken={}' # 表单实例
# url_3.format(team_response.json()['data']['accessToken'])

url_4 = 'https://www.yunzhijia.com/gateway/opendata-control/data/getperson?accessToken={}' # 个人员信息
# url_4.format(app_response.json()['data']['accessToken'])

url_5 = 'https://www.yunzhijia.com/gateway/opendata-control/data/getallpersons?accessToken={}' # 所有人员
# url_5.format(app_response.json()['data']['accessToken'])

# url_test = '/gateway/openimport/open/person/getall'
# url_test.format(app_response.json()['data']['accessToken'])

headers = {
    "Content-Type": "application/json"
}

# 获取accesstoken
def getaccesstoken():
    unix = int(time.time() * 1000)

    team_data = {'appId': 'SP13410137',
             'eid': '13410137',
             'secret': 'T2iFaqJkwdafR4ri3257x2WJ7VRBgU',
             'timestamp': unix,
             'scope': 'team'
            }
    
    app_data = {'appId': '500893729',
             'secret': '61zQdviLMMQGvyzNnkEr',
             'timestamp': unix,
             'scope': 'app'
            }
    
    resGroupSecret_data =  {
                        "eid": "13410137",
                        "secret": "IPGx7HUPuFbQk1gEGeapszRqz7Dbgx1z",
                        "timestamp": unix,
                        "scope": "resGroupSecret"
                    }
    
    team_response = requests.post(url, data=json.dumps(team_data), headers=headers)
    app_response = requests.post(url, data=json.dumps(app_data), headers=headers)
    resGroupSecret_response = requests.post(url, data=json.dumps(resGroupSecret_data), headers=headers)
    return app_response, resGroupSecret_response, team_response


# 获取人员考情审批流程列表
def process_lis(start_time,end_time,team_response):
    process_list_data = {
                        "pageSize": 100,
                        "title": "人员出勤日报表",
                        "formCodeIds": ['f800191835604648bc363d0959066b7a'],
                        # "createTime": [int(time.time() * 1000)-3600*1000*24*7,int(time.time() * 1000)-3600*1000*24*4]
                        "createTime": [start_time,end_time]
                        }
    
    process_lis_response = requests.post(url_2.format(team_response.json()['data']['accessToken']), data=json.dumps(process_list_data), headers=headers)
    return process_lis_response


# 获取表单实例信息
def examples(formInstId,team_response):
    Examples_data = {
                        "formInstId":formInstId,
                        "formCodeId":"f800191835604648bc363d0959066b7a"
                        }
    Examples_response = requests.post(url_3.format(team_response.json()['data']['accessToken']), data=Examples_data)
    
    return Examples_response


# 获取员工个人信息
def people(openId,app_response):
    people_data = {
                    "openId": openId,
                    "eid":"13410137",
                    "time":int(time.time() * 1000)
                    }
    
    people_response = requests.post(url_4.format(app_response.json()['data']['accessToken']), data=people_data)
    return people_response

# 输入想要查询的时间转换为时间戳
def time_unix(date_str):
    # date_str = "2025-4-6"

    # 解析日期（时间默认00:00:00，时区为本地时区）
    dt = datetime.strptime(date_str, "%Y%m%d")
    
    # 转换为Unix时间戳（秒）
    timestamp = int(dt.timestamp())*1000
    return [timestamp,timestamp+3600*24*1000]

# 查询月人员请假时间
def month_unix(date_str):
    dt = datetime.strptime(date_str, "%Y%m%d")

    # 获取dt的天数
    
    timestamp = int(dt.timestamp())*1000  
    days = int(date_str[6:8])
    
    return [timestamp-3600*24*days*1000,timestamp]
          
