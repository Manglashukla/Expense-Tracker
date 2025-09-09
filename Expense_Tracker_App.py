import sqlite3
from tkinter import *
from tkcalendar import DateEntry
import tkinter.messagebox as mb
import tkinter.ttk as ttk

# Database connection
connector = sqlite3.connect('ExpenseTracker.db')
cursor = connector.cursor()
connector.execute('''
CREATE TABLE IF NOT EXISTS ExpenseTracker (
    ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Date TEXT,
    Payee TEXT,
    Description TEXT,
    Amount FLOAT,
    ModeOfPayment TEXT
)
''')
connector.commit()

# Tkinter window setup
root = Tk()
root.title('Expense Tracker')
root.geometry('675x450')
root.config(background="#00FFFF")

# Labels and Entries
Label(root, text="             ", bg="#00FFFF").grid(row=0, column=2)
Label(root, text="DASHBOARD", bg='#66CCCC').grid(row=1, column=2)
Label(root, text="             ", bg="#00FFFF").grid(row=2, column=2)

def add_expense():
    date = date_entry.get()
    payee = payee_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()
    mode_of_payment = mode_of_payment_entry.get()
    
    if not (date and payee and description and amount and mode_of_payment):
        mb.showerror('Error!', "All fields are required!")
        return
    
    connector.execute('''
    INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment)
    VALUES (?, ?, ?, ?, ?)
    ''', (date, payee, description, amount, mode_of_payment))
    connector.commit()
    mb.showinfo('Expense added', 'Expense added successfully!')
    clear_fields()
    display_expenses()

def remove_expense():
    try:
        selected_item = tree.selection()[0]
        expense_id = tree.item(selected_item)['values'][0]
        
        # Confirm deletion
        confirm = mb.askyesno('Confirm Deletion', 'Are you sure you want to delete this expense?')
        if confirm:
            cursor.execute('DELETE FROM ExpenseTracker WHERE ID=?', (expense_id,))
            connector.commit()
            tree.delete(selected_item)
            mb.showinfo('Expense removed', 'Expense removed successfully!')
    except IndexError:
        mb.showerror('Error!', 'Please select an item to remove')
    except sqlite3.Error as e:
        mb.showerror('Error!', f'An error occurred: {e}')

def display_expenses(start_date=None, end_date=None):
    for row in tree.get_children():
        tree.delete(row)
    
    if start_date and end_date:
        cursor.execute('SELECT * FROM ExpenseTracker WHERE Date BETWEEN ? AND ?', (start_date, end_date))
    else:
        cursor.execute('SELECT * FROM ExpenseTracker')
    
    rows = cursor.fetchall()
    for index, row in enumerate(rows, start=1):
        tree.insert('', 'end', values=(index, *row[1:]))


def clear_fields():
    date_entry.set_date('')
    payee_entry.delete(0, END)
    description_entry.delete(0, END)
    amount_entry.delete(0, END)
    mode_of_payment_entry.delete(0, END)

def show_expenses_between_dates():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    display_expenses(start_date, end_date)

# UI Elements
Label(root, text='Date', bg="#CCFFFF").grid(row=4, column=1)
date_entry = DateEntry(root)
date_entry.grid(row=4, column=2)

Label(root, text='Receiver', bg="#CCFFFF").grid(row=5, column=1)
payee_entry = Entry(root)
payee_entry.grid(row=5, column=2)

Label(root, text='Name of Expense', bg="#CCFFFF").grid(row=6, column=1)
description_entry = Entry(root)
description_entry.grid(row=6, column=2)

Label(root, text='Amount', bg="#CCFFFF").grid(row=7, column=1)
amount_entry = Entry(root)
amount_entry.grid(row=7, column=2)

Label(root, text='Mode of Payment', bg="#CCFFFF").grid(row=8, column=1)
mode_of_payment_entry = Entry(root)
mode_of_payment_entry.grid(row=8, column=2)

Label(root, text='Start Date', bg="#CCFFFF").grid(row=9, column=1)
start_date_entry = DateEntry(root)
start_date_entry.grid(row=9, column=2)

Label(root, text='End Date', bg="#CCFFFF").grid(row=10, column=1)
end_date_entry = DateEntry(root)
end_date_entry.grid(row=10, column=2)

Button(root, text='Add Expense', command=add_expense, bg="#99CCCC").grid(row=6, column=2, columnspan=5)
Button(root, text='Remove Expense', command=remove_expense, bg="#99CCCC").grid(row=7, column=2, columnspan=5)
Button(root, text='Show Expenses', command=display_expenses, bg="#99CCCC").grid(row=6, column=3, columnspan=5)
Button(root, text='Show Expenses Between Dates', command=show_expenses_between_dates, bg="#99CCCC").grid(row=9, column=3, columnspan=5)
Button(root, text='Exit', command=root.destroy, bg="#99CCCC").grid(row=7, column=3, columnspan=5)

# Treeview for displaying expenses
tree = ttk.Treeview(root, columns=('Serial Number', 'Date', 'Payee', 'Description', 'Amount', 'ModeOfPayment'), show='headings')
tree.column(0, anchor=CENTER, stretch=NO, width=50)
tree.column(1, anchor=CENTER, width=90)
tree.column(2, anchor=CENTER, width=120)
tree.column(3, anchor=CENTER, width=160)
tree.column(4, anchor=CENTER, width=100)
tree.column(5, anchor=CENTER, width=120)
tree.heading('Serial Number', text='S.No.')
tree.heading('Date', text='Date')
tree.heading('Payee', text='Receiver')
tree.heading('Description', text='Name of Expense')
tree.heading('Amount', text='Amount')
tree.heading('ModeOfPayment', text='Mode of Payment')
tree.grid(row=3, column=1, columnspan=5)

root.mainloop()