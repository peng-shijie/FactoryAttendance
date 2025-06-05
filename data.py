from get_data import *
import pandas as pd
import numpy as np

def data(ctime,md):
    app_response, resGroupSecret_response, team_response = getaccesstoken()

    # ctime = '20250406'
    # 获取审流程列表-指定时间范围
    
    if md == 'day':
        cunix = time_unix(ctime)
        attendance_list = process_lis(cunix[0],cunix[1],team_response)
        attendance_list = pd.DataFrame(attendance_list.json()['data']['list'])
        # 具体到天
        date_attendance_list =  attendance_list[attendance_list['serialNo'].str.contains(ctime)]
        date_attendance_list = date_attendance_list[['deptName','formInstId', 'serialNo', 'createName']]
    if md == 'month':
        cunix = month_unix(ctime)
        attendance_list = process_lis(cunix[0],cunix[1],team_response)
        attendance_list = pd.DataFrame(attendance_list.json()['data']['list'])
        # 具体到月
        date_attendance_list =  attendance_list[attendance_list['serialNo'].str.contains(ctime[:6])]
        date_attendance_list = date_attendance_list[['deptName','formInstId', 'serialNo', 'createName']]

    should_list = []
    Reality_list = []
    Flights_list = []

    # # 创建请假人信息表; 字段：部门，姓名，请假天数，请假类型, 是否住宿，班次
    columns = ['DeptName', 'Name', 'Day', 'Type', 'Accommodation']
    data_people = pd.DataFrame(columns=columns)
    DeptName = []
    Name = []
    Day = []
    Type = []
    Accommodation = []
    Flights = []
    formInstId = []

    Flights_dict ={'AaBaCcDd':"行政", 'IiJjKkLl':"白班", '2wA2d5rI':"夜班"}
    Ra_3 = {'AaBaCcDd':"是", 'EeFfGgHh':"否"}  # 是否住宿
    Ra_1 = {'AaBaCcDd':"事假", 'EeFfGgHh':"病假"}  # 请假类型

    for i in date_attendance_list['formInstId']:
        examples_data = examples(i,team_response).json()
        should_list.append(examples_data['data']['formInfo']['widgetMap']['Nu_0']['value']) # 应到
        Reality_list.append(examples_data['data']['formInfo']['widgetMap']['Nu_1']['value']) # 实到
        Flights_list.append(Flights_dict[examples_data['data']['formInfo']['widgetMap']['Ra_0']['value']]) # 班次
        # print(i,Flights_dict[examples_data['data']['formInfo']['widgetMap']['Ra_0']['value']])
        
        Flights_people = Flights_dict[examples_data['data']['formInfo']['widgetMap']['Ra_0']['value']]
        deptname_ = examples_data['data']['formInfo']['widgetMap']['_S_APPLY']['personInfo'][0]['dept'] # 部门
        try:
            people_list = examples_data['data']['formInfo']['detailMap']['Dd_2']['widgetValue']  # 人员信息列表
        except :
            continue
        for p in people_list:
            if len(p['Ps_3'])==0:
                break
            else:
                Name.append(people(p['Ps_3'][0],app_response).json()['data'][0]['name'])  # 人名
            if p['Nu_3'] == '':
                Day.append(1) 
            else:
                Day.append(float(p['Nu_3']))         # 请假天数
            if p['Ra_1'] == '':
                Type.append("事假")
            else:
                Type.append(Ra_1[p['Ra_1']])  # 请假类型

            if p['Ra_3'] == '':
                Accommodation.append("否")
            else:
                Accommodation.append(Ra_3[p['Ra_3']])  # 是否住宿
            DeptName.append(deptname_)   # 部门
            Flights.append(Flights_people)  # 班次
            formInstId.append(i) 
            
    date_attendance_list['Flights'] = Flights_list
    date_attendance_list['should'] = should_list
    date_attendance_list['Reality'] = Reality_list
    date_attendance_list['number_people'] = date_attendance_list['should'].astype(int) - date_attendance_list['Reality'].astype(int) # 未到人数

    data_people['DeptName'] = DeptName
    data_people['Name'] = Name
    data_people['Flights'] = Flights
    data_people['Day'] = Day
    data_people['Type'] = Type
    data_people['Accommodation'] = Accommodation
    data_people['formInstId'] = formInstId

    date_attendance_list.loc[-1,"should"], date_attendance_list.loc[-1,"Reality"]= date_attendance_list.should.astype(int).sum(), date_attendance_list.Reality.astype(int).sum()
    date_attendance_list.loc[-1,"number_people"] = date_attendance_list.number_people.sum()
    date_attendance_list.reset_index(drop='index',inplace=True)
    date_attendance_list.rename(columns={"deptName":"部门",
                                        "formInstId":"表单ID",
                                        "serialNo":"流水号",
                                        "createName":"提交人",
                                        "Flights":"班次",
                                        "should":"应出勤",
                                        "Reality":"实际出勤",
                                        "number_people":"未出勤人数",
                                        },inplace=True)

    data_people.rename(columns={"DeptName":"部门",
                                "Name":"姓名",
                                "Flights":"班次",
                                "Day":"请假天数",
                                "Type":"请假类型",
                                "Accommodation":"是否住宿",
                                "formInstId":"表单ID",
                                },inplace=True)

    return date_attendance_list, data_people

if __name__ == '__main__':
    ctime = '20250406'
    date_attendance_list,data_people = data(ctime)
    date_attendance_list.to_excel('./{}.xlsx'.format(ctime+"出勤信息"), index=False)
    data_people.to_excel('./{}.xlsx'.format(ctime+"请假人员"), index=False)