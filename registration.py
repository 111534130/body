import csv
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

REGISTRATIONS_FILE = 'registrations.csv'
ACTIVITIES_FILE = 'activities.csv'

# --- 你的 Gmail 設定 ---
GMAIL_USER = 'yo96152347@gmail.com'
GMAIL_PASSWORD = 'hegcxgwsqtzvoqge'  # 16位密碼（已去掉空格）

def send_success_email(receiver_email, name, activity_name, session):
    """報名成功自動寄信函式"""
    try:
        # 郵件內文
        content = f"""
親愛的 {name} 同學您好：

恭喜您已成功報名活動！以下是您的報名資訊：
------------------------------------
活動名稱：{activity_name}
選擇場次：{session}
------------------------------------

請準時出席，若需取消報名，請至系統「查詢報名紀錄」進行操作。
這是一封系統自動發送的信件，請勿直接回覆。

活動報名系統 敬上
        """
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = GMAIL_USER
        message['To'] = receiver_email
        message['Subject'] = Header(f'【報名成功通知】{activity_name}', 'utf-8')

        # 使用 SSL 連線寄送
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, [receiver_email], message.as_string())
        print(f"郵件已成功寄送至: {receiver_email}")
    except Exception as e:
        print(f"郵件寄送出錯: {e}")

def get_registrations(student_id=None):
    regs = []
    if not os.path.exists(REGISTRATIONS_FILE): return regs
    with open(REGISTRATIONS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = str(row.get('學號', '')).strip()
            target = str(student_id).strip() if student_id else None
            if target is None or sid == target:
                regs.append({
                    'name': row.get('姓名', '未知'),
                    'student_id': row.get('學號', '無'),
                    'email': row.get('Email', '無'),
                    'age': row.get('年齡', '0'),
                    'session': row.get('場次', '無'),
                    'activity_name': row.get('活動名稱', '未知活動')
                })
    return regs

def get_registrations_count(activity_name, session=None):
    all_regs = get_registrations()
    if session:
        return len([r for r in all_regs if r['activity_name'] == activity_name and r['session'] == session])
    return len([r for r in all_regs if r['activity_name'] == activity_name])

def sync_activity_remaining(activity_name):
    activities = []
    if not os.path.exists(ACTIVITIES_FILE): return
    with open(ACTIVITIES_FILE, 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
        fieldnames = reader[0].keys() if reader else ['活動名稱', '日期', '地點', '名額', '剩餘名額', '場次']
        for a in reader:
            if a['活動名稱'] == activity_name:
                count = get_registrations_count(activity_name)
                a['剩餘名額'] = str(max(0, int(a['名額']) - count))
            activities.append(a)
    with open(ACTIVITIES_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(activities)

def register_user(name, student_id, email, age, session, activity_name):
    file_exists = os.path.exists(REGISTRATIONS_FILE)
    with open(REGISTRATIONS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['姓名', '學號', 'Email', '年齡', '場次', '活動名稱'])
        if not file_exists: writer.writeheader()
        writer.writerow({
            '姓名': name, '學號': str(student_id).strip(), 'Email': email,
            '年齡': age, '場次': session, '活動名稱': activity_name
        })
    sync_activity_remaining(activity_name)

def cancel_registration(student_id, activity_name):
    if not os.path.exists(REGISTRATIONS_FILE): return
    all_regs = []
    with open(REGISTRATIONS_FILE, 'r', encoding='utf-8') as f:
        all_regs = list(csv.DictReader(f))
    target_id = str(student_id).strip()
    new_regs = [r for r in all_regs if not (str(r.get('學號', '')).strip() == target_id and r.get('活動名稱', '') == activity_name)]
    with open(REGISTRATIONS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['姓名', '學號', 'Email', '年齡', '場次', '活動名稱'])
        writer.writeheader()
        writer.writerows(new_regs)
    sync_activity_remaining(activity_name)