import sqlite3
import hashlib

# 创建数据库连接
def connect_db():
    return sqlite3.connect("users.db")

# 创建用户表
def create_usertable():
    conn = connect_db()
    c = conn.cursor()
    # 创建用户表，包含用户名、密码和高分
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            highscore INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# 添加用户
def add_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    hashed_password = hash_password(password)  # 对密码进行哈希处理
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()

# 登录用户
def login_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    hashed_password = hash_password(password)  # 哈希输入的密码
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    data = c.fetchone()
    conn.close()
    return data is not None

# 哈希密码
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 更新用户信息
def update_user(username, new_username, new_password):
    conn = connect_db()
    c = conn.cursor()
    if new_password:
        hashed_new_password = hash_password(new_password)
        c.execute('UPDATE users SET username = ?, password = ? WHERE username = ?', (new_username, hashed_new_password, username))
    else:
        c.execute('UPDATE users SET username = ? WHERE username = ?', (new_username, username))
    conn.commit()
    conn.close()

# 删除用户
def delete_user(username):
    conn = connect_db()
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    conn.close()

# 更新用户的最高分
def update_highscore(username, score):
    conn = connect_db()
    c = conn.cursor()
    c.execute('UPDATE users SET highscore=? WHERE username=?', (score, username))
    conn.commit()
    conn.close()

# 获取用户的最高分
def get_highscore(username):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT highscore FROM users WHERE username=?', (username,))
    score = c.fetchone()
    conn.close()
    return score[0] if score else 0

def get_leaderboard():
    conn = connect_db()
    c = conn.cursor()
    # 查询所有用户及其最高分，按分数从高到低排序
    c.execute('SELECT username, highscore FROM users ORDER BY highscore DESC')
    leaderboard = c.fetchall()
    conn.close()
    return leaderboard

