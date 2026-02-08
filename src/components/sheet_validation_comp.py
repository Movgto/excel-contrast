from tkinter import Tk, StringVar, Button, Frame, Label, Entry, Text
from functions import validate_sheets

def sheet_validation_comp(container: Frame, filepath1: StringVar, filepath2: StringVar, validate_btn: Button):
    
    def on_button_clicked(event):
        for widget in container.winfo_children():
            widget.destroy()

        if (filepath1.get() == '' and filepath2.get() == ''): return
        
        (matches, diff1, diff2) = validate_sheets(filepath1=filepath1.get(), filepath2=filepath2.get())
        
        if (len(matches) > 0):
            Text(container)
        
        for sheet_name in matches:
            field_frame = Frame(container)
            field_frame.pack()
            
            label = Label(field_frame, text=f'Hoja {sheet_name} - Col. Id')
            label.pack(side='left')
            
            input = Entry(field_frame)
            input.pack(side='left')
            
            
    
    validate_btn.bind('<Button-1>', lambda e: on_button_clicked(e))
    