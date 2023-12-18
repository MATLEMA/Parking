from tkinter import *
from tkinter import ttk
from fonction import listing_port

# https://tkdocs.com/tutorial/index.html
# https://docs.python.org/3/library/tkinter.ttk.html#widget

root = Tk()
root.geometry("300x200")
root.resizable(False, False)
root.title("Parking")
fenetre = ttk.Frame(root, padding="10")

port_disponible = listing_port()
print(port_disponible)
combobox = ttk.Combobox(root, values = port_disponible, state= "readonly")
combobox.grid(row=0, column=0, padx=10, pady=10)

root.update()
root.mainloop()