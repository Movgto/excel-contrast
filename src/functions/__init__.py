from tkinter import filedialog, StringVar, Label, Entry
import pandas as pd
from pandas import DataFrame
from observer import Signal
import math

def truncate_to_5_decimals(x):
    """Convert to text, truncate decimals to 5 places, convert back to number."""
    if isinstance(x, (int, float)):
        str_x = str(x)
        if '.' in str_x:
            integer_part, decimal_part = str_x.split('.')
            truncated_decimal = decimal_part[:5]
            return float(f"{integer_part}.{truncated_decimal}")
        else:
            return float(str_x)
    else:
        return x


def normalize_name(name):
    """Normalize column names: lowercase and remove spaces/underscores."""
    return name.lower().replace(' ', '').replace('_', '')


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

def check_diferences(filepath1: str, filepath2: str, col_id_dict: dict[str, Entry], prog_bar_obs: Signal[float], sheet_mapping: dict[str, dict[str, str]]|None = None):
    f1 = pd.read_excel(filepath1, sheet_name=None)    
    prog_bar_obs.set(10)
    
    f2 = pd.read_excel(filepath2, sheet_name=None)    
    prog_bar_obs.set(20)
    
    result: dict[str, DataFrame] = {}
    
    segment = 40/len(col_id_dict)

    for display_name in col_id_dict.keys():
        # Usar el mapeo si está disponible, sino asumir que los nombres son iguales
        if sheet_mapping and display_name in sheet_mapping:
            sheet_a = sheet_mapping[display_name]['file1']
            sheet_b = sheet_mapping[display_name]['file2']
        else:
            sheet_a = display_name
            sheet_b = display_name
        
        sa = f1[sheet_a]
        sb = f2[sheet_b]
        
        # Normalize column names to ignore capitalization and separators (spaces/underscores)
        sa.columns = sa.columns.map(normalize_name)
        sb.columns = sb.columns.map(normalize_name)

        col_id = col_id_dict[display_name].get()
        
        # Normalize col_id to match normalized column names
        if col_id != "":
            col_id = normalize_name(col_id)
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
        
        sa_fill_blank = sa_fill_blank.map(truncate_to_5_decimals)
        sb_fill_blank = sb_fill_blank.map(truncate_to_5_decimals)

        differences = sa_fill_blank.compare(sb_fill_blank)

        result[display_name] = differences
        
        prog_bar_obs.set(prog_bar_obs.get() + segment)
    
    return result


    
def validate_sheets(filepath1: str, filepath2: str):
    f1 = pd.ExcelFile(filepath1)
    f2 = pd.ExcelFile(filepath2)
    
    sheets1 = set(f1.sheet_names)
    sheets2 = set(f2.sheet_names)
    
    # Diccionario para almacenar el mapeo de hojas
    sheet_mapping = {}
    matches = sheets1 & sheets2
    
    # Agregar hojas que coinciden por nombre
    for sheet in matches:
        sheet_mapping[sheet] = {'file1': sheet, 'file2': sheet}
    
    diff1 = sheets1 - sheets2
    diff2 = sheets2 - sheets1
    
    # Si ambos archivos tienen una sola hoja y no coinciden, mapearlas automáticamente
    if len(matches) == 0 and len(sheets1) == 1 and len(sheets2) == 1:
        sheet1 = list(sheets1)[0]
        sheet2 = list(sheets2)[0]
        display_name = f"{sheet1} → {sheet2}"
        sheet_mapping[display_name] = {'file1': sheet1, 'file2': sheet2}
        matches = {display_name}
        diff1 = set()
        diff2 = set()
    
    return matches, diff1, diff2, sheet_mapping
