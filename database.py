import sqlite3
import os
from tkinter import messagebox

def database_exists(db_file):
    return os.path.exists(db_file)

def create_database_and_table(db_name, db_type):
    db_dir = "Databases"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(current_dir, db_dir, f'{db_name}.db')

    if not os.path.exists(os.path.join(current_dir, db_dir)):
        os.makedirs(os.path.join(current_dir, db_dir))

    if not database_exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {db_name} (
                Date DATE, Second TEXT, Info TEXT, Mood TEXT, Diary_Type TEXT
            )
        ''')
        cursor.execute(f'''
            INSERT INTO {db_name} (Diary_Type) VALUES (?)
        ''', (db_type,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Database '{db_name}' with structure '{db_type}' created successfully")
    else:
        messagebox.showerror("Error", f"Diary with name '{db_name}' already exists")

def import_click(selected_diary, date_input, tasks_input, info_input, review_input):
    diary_name = selected_diary.split(" - ")[0]

    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = "Databases"
    db_file = os.path.join(current_dir, db_dir, f"{diary_name}.db")

    diary_type = "Personal" if "Personal" in selected_diary else "Programming"

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {diary_name} (Date, Second, Info, Mood, Diary_Type) VALUES (?, ?, ?, ?, ?)",
                           (date_input, tasks_input, info_input, review_input, diary_type))
        conn.commit()
    finally:
        if conn:
            conn.close()

def get_diaries():
    diaries = []
    db_dir = "Databases"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, db_dir)
    if os.path.exists(db_path) and os.path.isdir(db_path):
        for diary_file in os.listdir(db_path):
            if diary_file.endswith(".db"):
                diary_name = os.path.splitext(diary_file)[0]
                last_modified_time = os.path.getmtime(os.path.join(db_path, diary_file))
                last_modified_date = datetime.datetime.fromtimestamp(last_modified_time).strftime('%Y-%m-%d %H:%M:%S')
                diaries.append({"name": diary_name, "last_change": last_modified_date})
    return diaries
