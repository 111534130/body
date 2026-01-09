import csv
import os

ADMINS_FILE = 'admins.csv'
ACTIVITIES_FILE = 'activities.csv'

def check_admin_login(username, password):
    if not os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['帳號', '密碼'])
            writer.writerow(['admin', '1234'])
        return username == 'admin' and password == '1234'

    with open(ADMINS_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get('帳號') == username and row.get('密碼') == password:
                return True
    return False

def add_activity_admin(name, date, location, capacity, session):
    file_exists = os.path.isfile(ACTIVITIES_FILE)
    with open(ACTIVITIES_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['名稱', '日期', '地點', '名額', '場次'])
        writer.writerow([name, date, location, capacity, session])