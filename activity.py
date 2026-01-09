import csv
import os

ACTIVITIES_FILE = 'activities.csv'

def get_all_activities():
    activities = []
    if not os.path.exists(ACTIVITIES_FILE): return activities
    with open(ACTIVITIES_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            activities.append({
                'name': row['活動名稱'], 'date': row['日期'],
                'location': row['地點'], 'capacity': int(row['名額']),
                'remaining': int(row['剩餘名額']), 'session': row['場次']
            })
    return activities

def add_activity_admin(name, date, location, capacity, session):
    file_exists = os.path.exists(ACTIVITIES_FILE)
    with open(ACTIVITIES_FILE, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['活動名稱', '日期', '地點', '名額', '剩餘名額', '場次']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists: writer.writeheader()
        writer.writerow({'活動名稱': name, '日期': date, '地點': location, '名額': capacity, '剩餘名額': capacity, '場次': session})

def update_activity_admin(old_name, name, date, location, capacity, session):
    activities = get_all_activities()
    with open(ACTIVITIES_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['活動名稱', '日期', '地點', '名額', '剩餘名額', '場次'])
        writer.writeheader()
        for a in activities:
            if a['name'] == old_name:
                # 更新時要保持剩餘名額邏輯正確，這裡暫定為維持比例或手動重設
                writer.writerow({'活動名稱': name, '日期': date, '地點': location, '名額': capacity, '剩餘名額': capacity, '場次': session})
            else:
                writer.writerow({'活動名稱': a['name'], '日期': a['date'], '地點': a['location'], '名額': a['capacity'], '剩餘名額': a['remaining'], '場次': a['session']})