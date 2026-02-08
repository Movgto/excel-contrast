from tkinter import Tk, Toplevel, Label, Button

def popup_comp(root: Tk, text: str, title: str):
    popup = Toplevel(root)
    popup.title(title)
    
    popup.grab_set()
    
    label = Label(popup, text=text)
    label.pack(side='top', pady=10, fill='x')
    
    button = Button(text='Cerrar', pady=10)
    button.pack(command=popup.destroy)