from tkinter import *
from tkinter import ttk
import psycopg2 as psy
from tkinter import messagebox
import pandas as pd
from tkinter import filedialog

def run_query(query,parameters=()):
    conn=psy.connect(dbname="studentdb",user="postgres",password="123",host="localhost",port="5432")
    cur = conn.cursor()
    query_result = None
    try:
        cur.execute(query,parameters)
        if query.lower().startswith("select"):
            query_result=cur.fetchall()
        conn.commit()
    except psy.Error as e:
        messagebox.showerror("Database Error",str(e))
    finally:
        cur.close()
        conn.close()

    return query_result
def refresh_TreeView():
    for item in tree.get_children():
        tree.delete(item)
    records=run_query("select * from students;")
    for record in records:
        tree.insert('',END,values=record)


def insert_data():
    query = "insert into students(name,address,age,number) values (%s,%s,%s,%s)"
    parameters = (name_entry.get(),Adrees_enrty.get(),age.get(),phone.get())
    run_query(query,parameters)
    messagebox.showinfo("Information","Data inserted Successfully")
    refresh_TreeView()
def delete_data():
    selected_item=tree.selection()[0]
    student_id=tree.item(selected_item)['values'][0]
    query = "delete from students where student_id=%s"
    parameters = (student_id,)
    run_query(query,parameters)
    messagebox.showinfo("Information","Data deleted successfully")
    refresh_TreeView()

def update_data():
    selected_item=tree.selection()[0]
    student_id=tree.item(selected_item)['values'][0]
    query = "update students set name=%s,address=%s,age=%s,number=%s where student_id=%s"
    parameters = (name_entry.get(),Adrees_enrty.get(),age.get(),phone.get(),student_id)
    run_query(query,parameters)
    messagebox.showinfo("Information","Data updated successfully")
    refresh_TreeView()
def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS students (
        student_id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        address VARCHAR(200),
        age INT,
        number VARCHAR(15)
    )
    """
    run_query(query)
    messagebox.showinfo("Info", "Table created (if not exists).") 
def export_to_csv():
    records = run_query("SELECT * FROM students;")
    if records:
        df = pd.DataFrame(records, columns=["ID", "Name", "Address", "Age", "Number"])
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                 filetypes=[("CSV files","*.csv")])
        if file_path:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Export Success", f"Data exported to {file_path}")
    else:
        messagebox.showwarning("No Data", "No records available to export.")
def search_data():
    keyword = search_entry.get()
    for item in tree.get_children():
        tree.delete(item)
    query = "SELECT * FROM students WHERE name ILIKE %s"
    records = run_query(query, ('%' + keyword + '%',))
    for record in records:
        tree.insert('', END, values=record)
root = Tk()
root.title("Student Management System")
frame = LabelFrame(root,text="Student Data")
frame.grid(row=0,column=0,padx=10,pady=10,sticky="ew")

Label(frame,text="Name: ").grid(row=0,column=0,padx=2,pady=2,sticky="w")
name_entry = Entry(frame)
name_entry.grid(row=0,column=1,pady=2,sticky="ew")

Label(frame,text="Address: ").grid(row=1,column=0,padx=2,pady=2,sticky="w")
Adrees_enrty = Entry(frame)
Adrees_enrty.grid(row=1,column=1,pady=2,sticky="ew")

Label(frame,text="Age: ").grid(row=2,column=0,padx=2,pady=2,sticky="w")
age = Entry(frame)
age.grid(row=2,column=1,pady=2,sticky="ew")

Label(frame,text="Phone Entry: ").grid(row=3,column=0,padx=2,pady=2,sticky="w")
phone = Entry(frame)
phone.grid(row=3,column=1,pady=2,sticky="ew")

button_frame = Frame(root)
button_frame.grid(row=1,column=0,pady=5,sticky="ew")
search_frame = Frame(root)
search_frame.grid(row=3, column=0, pady=5, sticky="ew")

Label(search_frame, text="Search by Name: ").grid(row=0, column=0, padx=5)
search_entry = Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5)

Button(search_frame, text="Search", command=search_data).grid(row=0, column=2, padx=5)
Button(search_frame, text="Show All", command=refresh_TreeView).grid(row=0, column=3, padx=5)


Button(button_frame,text="Add Data",command=insert_data).grid(row=0,column=0,padx=5)
Button(button_frame,text="Create Table",command=create_table).grid(row=0,column=1,padx=5)
Button(button_frame,text="Update Data",command=update_data).grid(row=0,column=2,padx=5)
Button(button_frame,text="Delete Data",command=delete_data).grid(row=0,column=3,padx=5)
Button(button_frame, text="Export CSV", command=export_to_csv).grid(row=0, column=4, padx=5)

tree_frame = Frame(root)
tree_frame.grid(row=2,column=0,padx=10,sticky="nsew")

tree_scrollbar = Scrollbar(tree_frame)
tree_scrollbar.pack(side=RIGHT,fill=Y)

tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scrollbar.set,selectmode="browse")
tree.pack()
tree_scrollbar.config(command=tree.yview)


tree['columns'] = ("student_id","name","address","age","number")
tree.column("#0",width=0,stretch=NO)
tree.column("student_id",anchor=CENTER,width=80)
tree.column("name",anchor=CENTER,width=120)
tree.column("address",anchor=CENTER,width=120)
tree.column("age",anchor=CENTER,width=50)
tree.column("number",anchor=CENTER,width=120)

tree.heading("student_id",text="ID",anchor=CENTER)
tree.heading("name",text="Name",anchor=CENTER)
tree.heading("address",text="Address",anchor=CENTER)
tree.heading("age",text="Age",anchor=CENTER)
tree.heading("number",text="Number",anchor=CENTER)

refresh_TreeView()
root.mainloop()