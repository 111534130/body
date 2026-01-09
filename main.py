from admin import admin_login, show_registrations, add_admin
from activity import show_activity, add_activity
from registration import register, check_registration

def main_menu():
    print("\n===== 活動報名系統 =====")
    print("1. 查看活動資訊")
    print("2. 活動報名")
    print("3. 查詢報名狀態")
    print("4. 管理員登入")
    print("5. 離開")

while True:
    main_menu()
    choice = input("請選擇：")

    if choice == "1":
        show_activity()
    elif choice == "2":
        register()
    elif choice == "3":
        check_registration()
    elif choice == "4":
        if admin_login():
            while True:
                print("\n--- 管理員功能 ---")
                print("1. 新增活動")
                print("2. 查看報名名單")
                print("3. 新增管理員帳號")
                print("4. 返回主選單")

                sub = input("請選擇：")
                if sub == "1":
                    add_activity()
                elif sub == "2":
                    show_registrations()
                elif sub == "3":
                    add_admin()
                elif sub == "4":
                    break
                else:
                    print("輸入錯誤")
    elif choice == "5":
        print("系統結束")
        break
    else:
        print("輸入錯誤")
