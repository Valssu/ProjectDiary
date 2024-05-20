import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Listbox, Label, Entry, Button, Menu, END
import datetime
from database import create_database_and_table, import_click, get_diaries

global entry_date, entry_tasks, entry_info, entry_review, InputWindow, diary_listbox

def Home_page():
    def save_inputs():
        input_name = diary_name.get().strip()
        input_type = diary_type.get(diary_type.curselection())

        if not input_name or ' ' in input_name:
            messagebox.showerror("Error", "Diary Name cannot be empty or contain spaces.")
            return
        elif not input_type:
            messagebox.showerror("Error", "Please select a Diary Type.")
            return

        if any(char in input_name for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']):
            messagebox.showerror("Error", "Diary Name contains invalid characters.")
            return

        create_database_and_table(input_name, input_type)
    
    home_frame = tk.Frame(main_frame)

    label = tk.Label(main_frame, text="Diary Name:", bg='#211522', fg='white')
    label.place(x=90, y=50)

    diary_name = tk.Entry(main_frame, bg='#211522', fg='white')
    diary_name.place(x=170, y=50)

    lbl = Label(main_frame, text="Which type of diary?", bg='#211522', fg='white')
    diary_type = Listbox(main_frame, bg='#211522', fg='white')
    diary_type.insert(1, "Personal")
    diary_type.insert(2, "Programming")
    diary_type.insert(3, "Gym")

    lbl.place(x=130, y=90)
    diary_type.place(x=130, y=110)

    create_button = tk.Button(main_frame, text='New diary', bg='#211522', fg='white', command=save_inputs)
    create_button.place(x=130, y=300)
    home_frame.pack()

def open_selected():
    selection = diary_listbox.curselection()
    if selection:
        selected_diary = diary_listbox.get(selection[0])
        diary_name = selected_diary.split(" - ")[0]

        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = "Databases"
        db_file = os.path.join(current_dir, db_dir, f"{diary_name}.db")

        if os.path.exists(db_file):
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            try:
                cursor.execute(f"SELECT * FROM {diary_name} LIMIT -1 OFFSET 1")
                records = cursor.fetchall()

                if records: 
                    OutputWindow = Toplevel(root, bg='#211522')
                    OutputWindow.title(f"Entries for {diary_name}")
                    OutputWindow.geometry("400x400")

                    text_box = Text(OutputWindow, bg='#613659', fg='white')
                    text_box.pack(fill="both", expand=True)

                    def display_page(page_num, page_label):
                        text_box.delete('1.0', END)
                        start_index = (page_num - 1) * RECORDS_PER_PAGE
                        end_index = min(start_index + RECORDS_PER_PAGE, len(records))
                        for record in records[start_index:end_index]:
                            for i, field in enumerate(record):
                                if i != len(record) - 1:
                                    if field is not None:
                                        text_box.insert(END, f"{field}\n")
                            text_box.insert(END, "\n")
                        page_label.config(text=f"Page {page_num} of {num_pages}")

                    num_pages = (len(records) + RECORDS_PER_PAGE - 1) // RECORDS_PER_PAGE

                    page_label = Label(OutputWindow, text="")
                    page_label.pack(side="top", padx=10)
                    display_page(1, page_label)

                    def prev_page():
                        nonlocal current_page
                        if current_page > 1:
                            current_page -= 1
                            display_page(current_page, page_label)

                    def next_page():
                        nonlocal current_page
                        if current_page < num_pages:
                            current_page += 1
                            display_page(current_page, page_label)

                    current_page = 1
                    prev_button = Button(OutputWindow, text="Previous", command=prev_page)
                    prev_button.place(x=5, y=370)

                    next_button = Button(OutputWindow, text="Next", command=next_page)
                    next_button.place(x=360, y=370)
                else:
                    messagebox.showinfo("Empty Diary", "The selected diary does not contain any entries.")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("File Not Found", "The database file for the selected diary does not exist.")
    else:
        messagebox.showerror("Selection Error", "Please select a diary to open.")

def Input_window():
    global entry_date, entry_tasks, entry_info, entry_review, InputWindow

    if not diary_listbox.curselection():
        messagebox.showerror("Error", "Please select a diary before adding an entry.")
        return

    selected_index = diary_listbox.curselection()[0]
    selected_diary = diary_listbox.get(selected_index)
    diary_name = selected_diary.split(" - ")[0]

    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = "Databases"
    db_file = os.path.join(current_dir, db_dir, f"{diary_name}.db")

    if os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT Diary_Type FROM {diary_name}")
            diary_type = cursor.fetchone()[0]

            InputWindow = Toplevel(root, bg='#613659')
            InputWindow.title("New Window")
            InputWindow.geometry("200x250")

            label_date = Label(InputWindow, text="Date:", bg='#613659', fg='white')
            label_date.pack()
            entry_date = Entry(InputWindow)
            entry_date.pack()
            entry_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

            if diary_type == "Personal":
                label_tasks = Label(InputWindow, text="Title:", bg='#613659', fg='white')
            elif diary_type == "Programming":
                label_tasks = Label(InputWindow, text="Language:", bg='#613659', fg='white')
            elif diary_type == "Gym":
                label_tasks = Label(InputWindow, text="Muscle Group:", bg='#613659', fg='white')
            label_tasks.pack()
            entry_tasks = Entry(InputWindow)
            entry_tasks.pack()

            label_info = Label(InputWindow, text="More:", bg='#613659', fg='white')
            label_info.pack()
            entry_info = Text(InputWindow, height=2, width=20)
            entry_info.pack()

            label_review = Label(InputWindow, text="Mood:", bg='#613659', fg='white')
            label_review.pack()
            entry_review = Entry(InputWindow)
            entry_review.pack()

            button_import_click = Button(InputWindow, text="Write",
                                         command=lambda: (import_click(selected_diary, entry_date.get(), entry_tasks.get(), entry_info.get("1.0", END).strip(), entry_review.get()), InputWindow.destroy()))
            button_import_click.pack(pady=5)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred while accessing the Diary: {e}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Diary does not exist.")

def Read_page():
    Read_frame = tk.Frame(main_frame, bg='#211522')
    Read_frame.pack(fill='both', expand=True)

    header_label = tk.Label(Read_frame, text="Diaries and Last Changes", font=("Bold", 20), bg='#211522', fg='white')
    header_label.pack(pady=10)

    global diary_listbox
    diary_listbox = Listbox(Read_frame, bg='#211522', fg='white', width=40, height=10)
    diaries = get_diaries()

    for diary in diaries:
        diary_listbox.insert(END, f"{diary['name']} - Last Change: {diary['last_change']}")
    diary_listbox.pack(pady=20)

    diary_listbox.bind("<Button-3>", show_menu)

    open_button = tk.Button(Read_frame, text='Open Diary', bg='#211522', fg='white', command=open_selected)
    open_button.pack(pady=10)
    open_button = tk.Button(Read_frame, text='Input selected', bg='#211522', fg='white', command=Input_window)
    open_button.pack(pady=10)

    global output_text
    output_text = Text(Read_frame, width=60, height=10, bg='#211522', fg='white')
    output_text.pack(pady=10)
    Read_frame.pack(pady=20)

def delete_selected():
    selection = diary_listbox.curselection()
    if selection:
        diary_name = diary_listbox.get(selection[0]).split(" - ")[0]
        db_dir = "Databases"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_file = os.path.join(current_dir, db_dir, f"{diary_name}.db")
        try:
            os.remove(db_file)
            messagebox.showinfo("Success", f"Diary '{diary_name}' deleted successfully")
            Read_page()
        except FileNotFoundError:
            messagebox.showerror("Error", f"Diary '{diary_name}' does not exist")

def show_menu(event):
    menu = Menu(root, tearoff=0)
    menu.add_command(label="Open Diary", command=open_selected)
    menu.add_command(label="Input selected", command=Input_window)
    menu.add_separator()
    menu.add_command(label="Delete", command=delete_selected)
    menu.post(event.x_root, event.y_root)

def hide_indicators():
    Home_indicate.config(bg='#613659')
    Read_indicate.config(bg='#613659')

def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()

def indicate(lb, page):
    hide_indicators()
    lb.config(bg='white')
    delete_pages()
    page()
