from flask import Flask, render_template, request, redirect, url_for
from activity import get_all_activities, update_activity_admin, add_activity_admin
from registration import register_user, get_registrations, get_registrations_count, cancel_registration, send_success_email
from admin import check_admin_login
import os

app = Flask(__name__)

# 取得跑馬燈公告內容
def get_marquee_text():
    if os.path.exists('announcement.txt'):
        with open('announcement.txt', 'r', encoding='utf-8') as f:
            return f.read()
    return "歡迎來到活動報名系統！"

# 首頁
@app.route('/')
def index():
    return render_template("index.html", 
                           activities=get_all_activities(), 
                           announcement=get_marquee_text())

# 報名頁面 (包含自動寄信)
@app.route('/register/<activity_name>', methods=['GET', 'POST'])
def register(activity_name):
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        email = request.form['email']
        age = int(request.form['age'])
        session = request.form['session']
        
        # 1. 執行報名
        register_user(name, student_id, email, age, session, activity_name)
        
        # 2. 自動寄信
        try:
            send_success_email(email, name, activity_name, session)
        except Exception as e:
            print(f"自動寄信失敗: {e}")
            
        return render_template("success.html", name=name, activity_name=activity_name)
    
    curr = next((a for a in get_all_activities() if a['name'] == activity_name), None)
    sessions = [s.strip() for s in curr['session'].split(',')] if curr else []
    remains = {s: curr['capacity'] - get_registrations_count(activity_name, s) for s in sessions}
    return render_template("register.html", activity_name=activity_name, sessions_remaining=remains)

# 查詢報名紀錄
@app.route('/check', methods=['GET', 'POST'])
def check():
    results = []
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        results = get_registrations(student_id)
    return render_template("check.html", results=results)

# 取消報名
@app.route('/cancel', methods=['POST'])
def cancel():
    student_id = request.form['student_id']
    activity_name = request.form['activity_name']
    cancel_registration(student_id, activity_name)
    return redirect(url_for('check'))

# 管理員登入
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_admin_login(username, password):
            return redirect(url_for('admin_dashboard'))
        else:
            error = '帳號或密碼錯誤'
    return render_template("admin_login.html", error=error)

# 管理員儀表板
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template("admin_dashboard.html", 
                           activities=get_all_activities(), 
                           announcement=get_marquee_text())

# 新增活動
@app.route('/add_activity', methods=['GET', 'POST'])
def add_activity():
    if request.method == 'POST':
        add_activity_admin(
            request.form['name'], 
            request.form['date'], 
            request.form['location'], 
            int(request.form['capacity']), 
            request.form['session']
        )
        return redirect(url_for('admin_dashboard'))
    return render_template("add_activity.html")

# 編輯活動
@app.route('/edit_activity/<activity_name>', methods=['GET', 'POST'])
def edit_activity(activity_name):
    if request.method == 'POST':
        update_activity_admin(
            activity_name, 
            request.form['name'], 
            request.form['date'], 
            request.form['location'], 
            int(request.form['capacity']), 
            request.form['session']
        )
        return redirect(url_for('admin_dashboard'))
    curr = next((a for a in get_all_activities() if a['name'] == activity_name), None)
    return render_template("edit_activity.html", a=curr)

# 更新公告內容
@app.route('/update_announcement', methods=['POST'])
def update_announcement():
    content = request.form.get('announcement_content')
    with open('announcement.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    return redirect(url_for('admin_dashboard'))

# 管理員查看活動詳細統計與名單
@app.route('/admin/activity/<activity_name>')
def admin_activity_detail(activity_name):
    all_regs = [r for r in get_registrations() if r['activity_name'] == activity_name]
    stats = {"19-30": 0, "31-50": 0, "51+": 0}
    for r in all_regs:
        try:
            age = int(r['age'])
            if 19 <= age <= 30: stats["19-30"] += 1
            elif 31 <= age <= 50: stats["31-50"] += 1
            elif age > 50: stats["51+"] += 1
        except: pass 
    return render_template("admin_activity_detail.html", activity_name=activity_name, registrations=all_regs, age_stats=stats)

# --- 【新增功能】管理者手動重寄郵件 ---
@app.route('/admin/resend_email', methods=['POST'])
def admin_resend_email():
    name = request.form.get('name')
    email = request.form.get('email')
    activity_name = request.form.get('activity_name')
    session = request.form.get('session')
    try:
        send_success_email(email, name, activity_name, session)
        return f'<script>alert("已補發信件給 {name}！"); window.location.href="/admin/activity/{activity_name}";</script>'
    except Exception as e:
        return f'<script>alert("補發失敗: {e}"); window.history.back();</script>'

if __name__ == '__main__':
    app.run(debug=True)