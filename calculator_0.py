import tkinter as tk

root = tk.Tk()
menu = tk.Menu(root)
root.config(menu=menu)
file_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)

entry = tk.Entry(root, font=("Arial", 24), width=15, bd=10)
entry.grid(row=0, column=0, columnspan=4)

result_value = 0

def update_readout():
    entry.delete(0, tk.END)
    entry.insert(0, result_value)

def clear_entry():
    global result_value
    result_value = 0
    update_readout()

def error_message(msg):
    error_label = tk.Label(root, text=msg, font=("Arial", 12), fg="red")
    error_label.grid(row=4, column=0, columnspan=4)

# Add your operation functions here...

root.mainloop()