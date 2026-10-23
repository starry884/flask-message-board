from datetime import datetime
from pathlib import Path

import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-secret-key-please-change"   # flash 消息需要

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "messages.db"


def get_conn():
    """获取数据库连接，并让查询结果可以按列名访问。"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """首次运行时创建表（已存在则跳过）。"""
    conn = get_conn()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT NOT NULL,
                content    TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


@app.route("/")
def index():
    """首页：按 id 倒序展示所有留言。"""
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT id, name, content, created_at FROM messages ORDER BY id DESC"
        ).fetchall()
    finally:
        conn.close()
    return render_template("index.html", messages=rows)


@app.route("/add", methods=["POST"])
def add_message():
    """发布留言：校验 → 写库 → 重定向。"""
    name = (request.form.get("name") or "").strip()
    content = (request.form.get("content") or "").strip()

    # 后端校验不能省，前端 required 可以被绕过
    if not name or not content:
        flash("昵称和留言内容不能为空")
        return redirect(url_for("index"))
    if len(name) > 20:
        flash("昵称不能超过 20 个字符")
        return redirect(url_for("index"))
    if len(content) > 200:
        flash("留言内容不能超过 200 个字符")
        return redirect(url_for("index"))

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO messages (name, content, created_at) VALUES (?, ?, ?)",
            (name, content, created_at),      # 参数化查询，防 SQL 注入
        )
        conn.commit()
    finally:
        conn.close()

    flash("留言发布成功")
    return redirect(url_for("index"))


@app.route("/delete/<int:message_id>", methods=["POST"])
def delete_message(message_id):
    """删除留言：只允许 POST，避免被链接 / 爬虫误删。"""
    conn = get_conn()
    try:
        cur = conn.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        conn.commit()
        deleted = cur.rowcount
    finally:
        conn.close()

    flash("留言已删除" if deleted else "留言不存在或已被删除")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)