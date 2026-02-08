from tkinter import filedialog, StringVar, Label, Entry
import pandas as pd
from pandas import DataFrame
from observer import Signal

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

def check_diferences(filepath1: str, filepath2: str, col_id_dict: dict[str, Entry], prog_bar_obs: Signal[float]):
    f1 = pd.read_excel(filepath1, sheet_name=None)    
    prog_bar_obs.set(10)
    
    f2 = pd.read_excel(filepath2, sheet_name=None)    
    prog_bar_obs.set(20)
    
    result: dict[str, DataFrame] = {}
    
    segment = 40/len(col_id_dict)

    for sheet_name in col_id_dict.keys():
        sa = f1[sheet_name]
        sb = f2[sheet_name]

        col_id = col_id_dict[sheet_name].get()
        
        if col_id != "":
            sa = sa.set_index(col_id)
            sb = sb.set_index(col_id)

        all_indexes = sa.index.union(sb.index)
        all_col = sa.columns.union(sb.columns)

        sa_fill_blank = sa.reindex(index=all_indexes, columns=all_col)
        sb_fill_blank = sb.reindex(index=all_indexes, columns=all_col)
        
        print('Sheet A:')
        print(sa_fill_blank.to_string())
        
        print('Sheet B:')
        print(sb_fill_blank.to_string())                

        differences = sa_fill_blank.compare(sb_fill_blank)

        result[sheet_name] = differences
        
        prog_bar_obs.set(prog_bar_obs.get() + segment)
    
    return result


    
def validate_sheets(filepath1: str, filepath2: str):
    f1 = pd.ExcelFile(filepath1)
    f2 = pd.ExcelFile(filepath2)
    
    sheets1 = set(f1.sheet_names)
    sheets2 = set(f2.sheet_names)
    
    matches = sheets1 & sheets2
    
    diff1 = sheets1 - sheets2
    diff2 = sheets2 - sheets1
    
    return matches, diff1, diff2
