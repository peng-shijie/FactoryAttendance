# 🚀 FactoryAttendance

## 🏭 项目简介

FactoryAttendance 是一个用 Python 编写的考勤信息获取与统计分析工具。该项目通过 API 接口获取工厂员工的考勤数据，并对数据进行整理、统计与分析，帮助管理人员高效掌握员工出勤状况，提升工厂运营管理效率。

## ✨ 主要功能

- 🔗 **API 数据获取**：通过对接考勤系统或相关 API，自动获取员工考勤原始数据。
- 🧹 **数据清洗与整理**：对原始考勤数据进行格式标准化、异常数据筛查与修正。
- 📊 **统计分析**：自动统计出勤率、迟到早退、缺勤等关键考勤指标。
- 📑 **报表生成**：输出多维度统计报表，便于管理层快速掌握整体和个体考勤情况。
- 🧩 **自定义扩展**：支持根据需要扩展新的数据分析或报表输出功能。

## ⚙️ 安装与使用

1. **克隆仓库**
   ```bash
   git clone https://github.com/shijiepeng/FactoryAttendance.git
   cd FactoryAttendance
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置 API 访问参数**
   - 编辑配置文件（如有），填写 API 地址、密钥等必要参数。

4. **运行项目**
   ```bash
   streamlit run app.py
   ```

## 🗂️ 目录结构

```
FactoryAttendance/
├── get_data/           # API接口相关代码
├── data/          # 数据存储与处理
├── app.py        # 主程序入口
├── requirements.txt
└── README.md
```

## 🏆 适用场景

- 工厂或企业的自动化考勤统计与分析
- 多工厂、多部门的出勤情况汇总
- 管理层的决策支持数据报表

## 🤝 参与贡献

欢迎提交 issue 报告 bug 或建议，或通过 pull request 参与代码贡献。

## 📄 许可协议

本项目采用 MIT License，详情参见 LICENSE 文件。
