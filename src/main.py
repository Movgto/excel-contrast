import tkinter as tk
from tkinter import Entry, ttk
from functions import select_file, check_diferences
from components.sheet_validation_comp import sheet_validation_comp
from components.popup_comp import popup_comp
from observer import Signal
import os
import sys

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

sheets_dict_obs = Signal[dict[str, Entry]]({})

sheet_validation_comp(sheet_val_cont, filepath1=route_a, filepath2=route_b, validate_btn=validate_sheets_btn, sheets_obs=sheets_dict_obs)

compare_btn = tk.Button(window, text='Comparar archivos', state='disabled')

prog_bar_cont = tk.Frame(pady=10)

def on_compare_btn_click():
    compare_btn.config(state='disabled')
    progress_bar = ttk.Progressbar(prog_bar_cont, mode='determinate', orient='horizontal')
    
    progress_bar.config(maximum=100, value=0)
    
    progress_bar.pack()
    
    progress = Signal[float](0)
    
    def update_progress(value: float):
        progress_bar.config(value=value)
        prog_bar_cont.update_idletasks()
    
    progress_subs = progress.subscribe(update_progress)
    
    result = check_diferences(route_a.get(), route_b.get(), sheets_dict_obs.get(), prog_bar_obs=progress)

    print('Comparison result:')
    print(result)
    
    def cleanup():
        progress.unsubscribe(subs=progress_subs)
    
        compare_btn.config(state='active')
        progress_bar.destroy()
    
    if all([df.empty for df in result.values()]):
        cleanup()
        popup_comp(window, 'No se encontraron diferencias en los archivos', 'No hay diferencias!')
        return
    
    current_dir = ''

    if getattr(sys, 'frozen', False):
        current_dir = os.path.dirname(sys.executable)
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    
    
    dir = os.path.join(current_dir, 'results')
    
    os.makedirs(dir, exist_ok=True)
    
    segment = 40/len(result)     
        
    for sheet_name in result.keys():    
        file_path = os.path.join(dir, f'result_{sheet_name}.xlsx')
        result[sheet_name].to_excel(file_path)
        
        progress.set(min(progress.get() + segment, 100))
        
    progress.set(100)
    
    cleanup()

compare_btn.bind('<Button-1>', lambda e: on_compare_btn_click())
compare_btn.pack(pady=10)

prog_bar_cont.pack(fill='x')

file1button.bind('<Button-1>', lambda e: compare_btn.config(state='disabled'))
file2button.bind('<Button-1>', lambda e: compare_btn.config(state='disabled'))

def update_compare_btn(sheets_dict: dict[str, Entry]):
    if len(sheets_dict) > 0:
        compare_btn.config(state='active')

sheets_dict_obs.subscribe(update_compare_btn)

window.mainloop()