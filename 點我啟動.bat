@echo off
echo 🚀 正在啟動活動報名系統...
cd /d "C:\Users\User\Desktop\body"

:: 啟動虛擬環境
call .\venv\Scripts\activate

:: 自動開啟瀏覽器 (5秒後)
timeout /t 5 /nobreak > nul
start http://127.0.0.1:5000

:: 運行 Python
python app.py

pause