from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'huy'

# Kết nối đến cơ sở dữ liệu SQLite
def connect_db():
    conn = sqlite3.connect('db/Account.db')
    return conn

# Route để hiển thị trang đăng ký
@app.route('/register', methods=['GET'])
def show_register_form():
    return render_template('register.html')

# Route để xử lý đăng ký
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Tên người dùng đã tồn tại. Vui lòng chọn tên người dùng khác.')
            conn.close()
            return redirect(url_for('show_register_form'))
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Đăng ký thành công! Hãy đăng nhập ngay.')
            conn.close()
            return redirect(url_for('login'))

# Route để hiển thị trang đăng nhập
@app.route('/login', methods=['GET'])
def show_login_form():
    return render_template('login.html')

# Route để xử lý đăng nhập
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return "Đăng nhập thành công!"
        else:
            return "Tên người dùng hoặc mật khẩu không hợp lệ. Vui lòng thử lại."

if __name__ == '__main__':
    app.run(debug=True)
