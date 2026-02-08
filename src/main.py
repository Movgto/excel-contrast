import tkinter as tk
from functions import select_file
from components.sheet_validation_comp import sheet_validation_comp

window = tk.Tk()

window.title('Comparador de Excel')
window.geometry('600x500')

route_a = tk.StringVar()
route_b = tk.StringVar()

lbl_file1button = tk.Label(window, text='Archivo A: No Seleccionado', fg='blue')
lbl_file1button.pack(pady=5)
file1button = tk.Button(window, text='Cargar archivo A', command=lambda: select_file(route_a, lbl_file1button))
file1button.pack(pady=20)

lbl_file2button = tk.Label(window, text='Archivo B: No Seleccionado', fg='blue')
lbl_file2button.pack(pady=5)
file2button = tk.Button(window, text='Cargar archivo B', command=lambda: select_file(route_b, lbl_file2button))
file2button.pack(pady=20)

validate_sheets_btn = tk.Button(window, text='Validar hojas')
validate_sheets_btn.pack()

sheet_val_cont = tk.Frame(window)
sheet_val_cont.pack()

sheet_validation_comp(sheet_val_cont, filepath1=route_a, filepath2=route_b, validate_btn=validate_sheets_btn)

window.mainloop()