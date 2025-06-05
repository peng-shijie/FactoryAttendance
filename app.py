import streamlit as st
import pandas as pd
import numpy as np
from get_data import *
from data import *
import matplotlib.pyplot as plt
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
# pd.set_option("display.max_colwidth", None)

st.set_page_config(page_title="考勤信息查询", layout="wide")

@st.cache_data
def load_data(user_input,md):
    date_attendance_list, data_people = data(user_input,md)
    return date_attendance_list, data_people


st.sidebar.title("用户输入")
user_input = st.sidebar.text_input("请输入查询日期例如：20220101")

try:
    if user_input:
        if len(user_input) != 8:
            st.sidebar.error("日期格式错误，请重新输入")
        else:
            date_attendance_list,data_people = load_data(user_input,md='day')
            _,month_data_people = load_data(user_input,md='month')
except:
    pass


    


st.sidebar.title("请选择操作")
option = st.sidebar.radio(
    "选择一个功能",
    ("人员出勤数据", "考勤统计分析")
)

try:
    if option == "人员出勤数据":

        st.markdown(
        """
        <h1 style="text-align: center;">📊 人员出勤信息查询</h1>
        """, 
        unsafe_allow_html=True
        )
        
        x = date_attendance_list.iloc[:-1,:].query("未出勤人数>0").sort_values(by=['未出勤人数'], ascending=False)['部门'].tolist()
        y = date_attendance_list.iloc[:-1,:].query("未出勤人数>0").sort_values(by=['未出勤人数'], ascending=False)['未出勤人数'].tolist()
        def create_bar_chart():
            bar = (
                Bar()
                .add_xaxis(x)
                .add_yaxis("人数",y,label_opts=opts.LabelOpts(position="top"))
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="部门请假人数"),
                    xaxis_opts=opts.AxisOpts(name="部门"),
                    yaxis_opts=opts.AxisOpts(name="人数"),
                )
            )
            return bar

        chart1 = create_bar_chart()
        st_pyecharts(chart1)  # 直接渲染图表


        col1, col2 = st.columns([2, 1]) 

        with col1:
            st.markdown(
                """
                <h4>部门出勤统计表</h4>
                """, 
                unsafe_allow_html=True
            )
            st.dataframe(date_attendance_list)

        with col2:
            st.markdown(
                """
                <h4>请假人员信息表</h4>
                """, 
                unsafe_allow_html=True
            )
            st.dataframe(data_people.iloc[:,:-1])

        depreplace = {'机加班':'机加部','打磨班':'清理美容基地','质量班':'质管部','毛坯终检班':'清理美容基地'}
        df_merged = pd.merge(date_attendance_list, data_people.drop(['部门','班次'],axis=1), on='表单ID', how='left').drop(['流水号','提交人','请假天数'],axis=1)
        df_merged['姓名'] = df_merged['姓名']+df_merged['请假类型']
        df_merged.drop('请假类型',axis=1,inplace=True)
        df_merged['部门'] = df_merged['部门'].replace(depreplace)

        agg_dict = {
            '应出勤': 'first',          
            '实际出勤': 'first',        
            '未出勤人数': 'first',     
            '姓名': lambda x: ', '.join(x.dropna().astype(str)),  
            '是否住宿': lambda x: '是' if (x == '是').any() else '否'
        }

        # 分组聚合
        # df_merged = df_merged.groupby(['部门', '班次']).agg(agg_dict)
        df_merged = df_merged.groupby(['部门', '班次','表单ID']).agg(agg_dict).reset_index()
        df_merged.drop('表单ID',axis=1,inplace=True)
        df_merged.loc[-1,'应出勤'] = df_merged['应出勤'].astype(float).sum()
        df_merged.loc[-1,'实际出勤'] = df_merged['实际出勤'].astype(float).sum()
        df_merged.loc[-1,'未出勤人数'] = df_merged['未出勤人数'].astype(float).sum()



        st.markdown(
            """
            <h4>部门出勤-人员信息表</h4>
            """, 
            unsafe_allow_html=True
        )
        st.dataframe(df_merged)

    if option == "考勤统计分析":

        st.markdown(
        """
        <h1 style="text-align: center;">📊 考勤统计分析</h1>
        """, 
        unsafe_allow_html=True
        )

        st.markdown(
            """
            <h4>{}月{}日未报部门及请假人员统计</h4>
            """.format(user_input[4:6],user_input[6:8]), 
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 1]) 
        
        with col1:
            deptname_list = ['营销部','技术一部','技术二部','生产部','铸造部','机加部',
                            '清理美容基地','质管部','物资部','检测中心','综合部','财务部',
                            '人力资源部','大数据中心','管理部','保全部']
            depreplace = {'机加班':'机加部','打磨班':'清理美容基地','质量班':'质管部','毛坯终检班':'清理美容基地'}
            missing_depts = [dept for dept in deptname_list if dept not in date_attendance_list['部门'].replace(depreplace).values]
            str1 = ''
            for i in range(len(missing_depts)):
                str1 += str(i+1)+'. '
                str1 += missing_depts[i] + '\n'
            st.markdown(
                str1, 
                unsafe_allow_html=True
                )

        with col2:
            
            col3,col4=st.columns(2) 
            col3.markdown("<h4 font-weight: bold;'>未出勤人数</h4>", unsafe_allow_html=True)
            col3.metric(label="", value=date_attendance_list.iloc[-1]['未出勤人数'])
            col4.markdown("<h4 font-weight: bold;'>请假人数</h4>", unsafe_allow_html=True)
            col4.metric(label="", value=data_people.shape[0]) 


        st.markdown(
            """
            <h4></h4>
            """, 
            unsafe_allow_html=True
        )

        month_ = month_data_people.groupby('姓名').agg(部门=('部门', 'first'),总天数=('请假天数', 'sum')).reset_index()
        month_.sort_values('总天数',ascending=True,inplace=True)
        categories = month_.iloc[-10:,:]['姓名'].tolist()
        values = month_.iloc[-10:,:]['总天数'].tolist()
        def create_horizontal_bar_chart():
            bar = (
                Bar()
                .add_xaxis(categories)  
                .add_yaxis("请假天数", values)  
                .reversal_axis()  
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="月员工请假天数统计"),  
                    xaxis_opts=opts.AxisOpts(name="请假天数"),  #
                    yaxis_opts=opts.AxisOpts(name="姓名"),  # 
                )
                .set_series_opts(
                    label_opts=opts.LabelOpts(position="right")
                )
            )
            return bar

        chart2 = create_horizontal_bar_chart()
        st_pyecharts(chart2) 


        col5, col6 = st.columns([1, 1]) 

        with col5:
            st.markdown(
                """
                <h4>{}月请假人员信息表</h4>
                """.format(user_input[4:6]), 
                unsafe_allow_html=True
            )

            st.dataframe(month_data_people)
        
        with col6:
            st.markdown(
                """
                <h4>请假天数统计</h4>
                """, 
                unsafe_allow_html=True
            )
            
            st.dataframe(month_)

except:
    pass