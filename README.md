# Flask 留言板
一个基于 Flask + SQLite 的简单留言板，支持发布、展示和删除留言。


## 功能
- 发布留言（昵称 + 内容，后端校验非空与长度）
- 按时间倒序展示留言
- 删除留言（POST + 二次确认）
- 参数化查询防 SQL 注入


## 技术栈
- Python 3.10+
- Flask 3.x
- SQLite（Python 标准库 sqlite3）
- Jinja2 模板


## 项目结构
flask-message-board/
├── app.py                 # 主程序
├── templates/
│   ├── base.html          # 公共模板（含 flash 提示）
│   └── index.html         # 留言列表页
├── static/
│   └── style.css          # 简单样式
├── requirements.txt
├── README.md
└── .gitignore


## 环境准备
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 3. 安装 Flask
pip install flask


## 运行方式
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python app.py