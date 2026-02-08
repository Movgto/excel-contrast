from tkinter import filedialog, StringVar, Label
import pandas as pd

def select_file(routevar: StringVar, label: Label):
    route = filedialog.askopenfile(
        title='Seleccionar archivo excel',
        filetypes=[('Archivos de excel', '*.xlsx *.xls')]
    )        
    
    if route:
        print(f'Un archivo ha sido seleccionado: {route.name}')
        routevar.set(route.name)
        label.config(text=f'Seleccionado: {route.name.split('/')[-1]}')
        
    return route

def check_diferences(filepath1: str, filepath2: str):
    f1 = pd.read_excel(filepath1)
    f2 = pd.read_excel(filepath2)
    
    diff = f1.compare(f2)
    
def validate_sheets(filepath1: str, filepath2: str):
    f1 = pd.ExcelFile(filepath1)
    f2 = pd.ExcelFile(filepath2)
    
    sheets1 = set(f1.sheet_names)
    sheets2 = set(f2.sheet_names)
    
    matches = sheets1 & sheets2
    
    diff1 = sheets1 - sheets2
    diff2 = sheets2 - sheets1
    
    return matches, diff1, diff2
