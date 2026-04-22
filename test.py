import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create Students table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS Students (
    ID TEXT PRIMARY KEY,
    Name TEXT NOT NULL,
    Age INTEGER NOT NULL
)
''')
conn.commit()

# Functions for student management
def add_student():
    student_id = entry_id.get()
    name = entry_name.get()
    age = entry_age.get()

    if not student_id or not name or not age:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    try:
        cursor.execute('INSERT INTO Students (ID, Name, Age) VALUES (?, ?, ?)', 
                       (student_id, name, int(age)))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully.")
        display_students()
        clear_student_fields()
    except sqlite3.IntegrityError:
        messagebox.showwarning("Duplicate ID", "Student ID already exists.")

def delete_student():
    student_id = entry_delete.get()  # Getting input from the delete entry field
    if not student_id:
        messagebox.showwarning("Input Error", "Please enter an ID to delete.")
        return
    
    cursor.execute('DELETE FROM Students WHERE ID = ?', (student_id,))
    
    if cursor.rowcount:
        conn.commit()
        messagebox.showinfo("Success", "Student deleted.")
        display_students()
        clear_student_fields()
    else:
        messagebox.showwarning("Not Found", "No student found with that ID.")

def display_students():
    listbox.delete(0, tk.END)
    cursor.execute('SELECT * FROM Students')
    for row in cursor.fetchall():
        listbox.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

def search_students():
    search_term = entry_search.get()  # Getting input from the search entry field
    if not search_term:
        messagebox.showwarning("Input Error", "Please enter an ID or Name to search.")
        return
    
    listbox.delete(0, tk.END)
    
    # Search using either ID or Name
    cursor.execute('SELECT * FROM Students WHERE ID LIKE ? OR Name LIKE ?', 
                   ('%' + search_term + '%', '%' + search_term + '%'))
    results = cursor.fetchall()
    
    if not results:
        messagebox.showinfo("No Results", "No students found.")
    
    for row in results:
        listbox.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

def clear_student_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_search.delete(0, tk.END)  # Clear search field too
    entry_delete.delete(0, tk.END)  # Clear delete field too

# UI setup
root = tk.Tk()
root.title("Student Management System")
root.geometry("900x650")  # Increased window size

# Student form frame
form_frame = tk.Frame(root)
form_frame.pack(pady=20)

tk.Label(form_frame, text="Student ID").grid(row=0, column=0, padx=10, pady=10)
entry_id = tk.Entry(form_frame)
entry_id.grid(row=0, column=1)

tk.Label(form_frame, text="Name").grid(row=1, column=0, padx=10, pady=10)
entry_name = tk.Entry(form_frame)
entry_name.grid(row=1, column=1)

tk.Label(form_frame, text="Age").grid(row=2, column=0, padx=10, pady=10)
entry_age = tk.Entry(form_frame)
entry_age.grid(row=2, column=1)

# Search Entry
tk.Label(form_frame, text="Search by ID or Name").grid(row=3, column=0, padx=10, pady=10)
entry_search = tk.Entry(form_frame)
entry_search.grid(row=3, column=1)

# Delete Entry
tk.Label(form_frame, text="Delete by ID").grid(row=4, column=0, padx=10, pady=10)
entry_delete = tk.Entry(form_frame)
entry_delete.grid(row=4, column=1)

# Buttons for student management
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

tk.Button(button_frame, text="Add Student", command=add_student, width=15).grid(row=0, column=0, padx=10, pady=10)
tk.Button(button_frame, text="Delete Student", command=delete_student, width=15).grid(row=0, column=1, padx=10, pady=10)
tk.Button(button_frame, text="Show All Students", command=display_students, width=15).grid(row=1, column=0, padx=10, pady=10)
tk.Button(button_frame, text="Search Students", command=search_students, width=15).grid(row=1, column=1, padx=10, pady=10)
tk.Button(button_frame, text="Clear Fields", command=clear_student_fields, width=15).grid(row=2, column=0, padx=10, pady=10)

# Listbox for displaying students
listbox_frame = tk.Frame(root)
listbox_frame.pack(pady=20)

listbox = tk.Listbox(listbox_frame, width=70, height=15)
listbox.pack()

# Start the application
root.mainloop()
conn.close()
