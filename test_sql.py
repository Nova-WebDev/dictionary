import sqlite3
import json
import os

# مسیر فایل دیتابیس (کنار main.py)
db_path = "database.db"

# اتصال به دیتابیس (اگه نباشه خودش می‌سازه)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ساخت جدول ترجمه‌ها (پشتیبانی از فارسی)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS translations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        meaning TEXT NOT NULL
    )
''')

# ساخت جدول کاربران
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        mail TEXT NOT NULL,
        password TEXT NOT NULL,
        authorization TEXT NOT NULL
    )
''')

# درج داده‌های ترجمه از dictionary.json
if os.path.exists("dictionary.json"):
    with open("dictionary.json", "r", encoding="utf-8") as f:
        translations = json.load(f)
        for word, meaning in translations.items():
            cursor.execute("INSERT INTO translations (word, meaning) VALUES (?, ?)", (word, meaning))
else:
    print("⚠️ فایل dictionary.json پیدا نشد.")

# درج داده‌های کاربران از users.json
if os.path.exists("users.json"):
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
        for username, info in users.items():
            cursor.execute('''
                INSERT INTO users (username, mail, password, authorization)
                VALUES (?, ?, ?, ?)
            ''', (username, info["mail"], info["password"], info["authorization"]))
else:
    print("⚠️ فایل users.json پیدا نشد.")

# ذخیره و بستن اتصال
conn.commit()
conn.close()

print("✅ فایل database.db ساخته شد و داده‌ها درج شدند.")
