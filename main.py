import tkinter as tk
from tkinter import messagebox
from gui import Home_page, Read_page, indicate

# Tkinter root 
root = tk.Tk()
root.geometry('600x400')
root.title("Programming Diary")
root.resizable(False, False)

# SIDE FRAME / OPTIONS
options_frame = tk.Frame(root, bg='#613659')
Home_button = tk.Button(options_frame, text="Home", font=("Bold", 15), fg='white', bd=0, bg='#613659', command=lambda: indicate(Home_indicate, Home_page))
Home_button.place(x=10, y=50)

Home_indicate= tk.Label(options_frame, text='', bg='#613659' )
Home_indicate.place(x=3, y=50, width=5, height=40)

Read_button = tk.Button(options_frame, text="Read", font=("Bold", 15), fg='white', bd=0, bg='#613659', command=lambda: indicate(Read_indicate, Read_page))
Read_button.place(x=10, y=100)

Read_indicate = tk.Label(options_frame, text='', bg='#613659')
Read_indicate.place(x=3, y=100, width=5, height=40)

options_frame.pack(side=tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=150, height=400)

# MAIN FRAME
main_frame = tk.Frame(root, highlightbackground='black', bg='#211522', highlightthickness=2)
main_frame.pack(side=tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(height=400, width=500)

root.mainloop()
