from tkinter import StringVar, Button, Frame, Label, Entry
from observer import Signal
from functions import validate_sheets

def sheet_validation_comp(container: Frame, filepath1: StringVar, filepath2: StringVar, validate_btn: Button, sheets_obs: Signal[dict[str, Entry]]):
    
    def on_button_clicked(event):
        for widget in container.winfo_children():
            widget.destroy()

        if (filepath1.get() == '' and filepath2.get() == ''):
            Label(container, text='No se encontraron hojas en común para comparar.').pack(pady=5)
            return
        
        (matches, diff1, diff2) = validate_sheets(filepath1=filepath1.get(), filepath2=filepath2.get())
        
        if (len(matches) > 0):
            Label(container, text='Estas son las hojas en común de ambos archivos. Indique cual es la columna de valores únicos si la hay, o deje el campo en blanco.',
                  wraplength=500
                  ).pack(
                fill='x',
                padx=20,
                pady=10
            )
        else:
            Label(container, text='No se encontraron hojas en común para comparar.', wraplength=200).pack()
        
        
        
        for sheet_name in matches:
            field_frame = Frame(container)
            field_frame.pack()
            
            label = Label(field_frame, text=f'Hoja {sheet_name} - Col. Id')
            label.pack(side='left', pady=5)
            
            input = Entry(field_frame)
            input.pack(side='left', pady=5)

            new_sheets_dict = sheets_obs.get()

            new_sheets_dict[str(sheet_name)] = input # This is not the ideal way to do it, but it's useful here.

        sheets_obs.set(sheets_obs.get()) # Resetting to the same value only to notify subscribers about the changes.         

        if len(diff1):
            Label(container, text='Hojas en A que no están en B')\
                .pack(
                    pady=10
                )
            
            Label(container, text=", ".join([str(sheet_name) for sheet_name in diff1]), wraplength=400)\
                .pack(
                    pady=10
                )
            
        if len(diff2):
            Label(container, text='Hojas en B que no están en A')\
                .pack(
                    pady=10
                )
            
            Label(container, text=", ".join([str(sheet_name) for sheet_name in diff2]), wraplength=400)\
                .pack(
                    pady=10
                )

        
            
            
    
    validate_btn.bind('<Button-1>', lambda e: on_button_clicked(e))
    