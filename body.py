from tkinter import *
from tkinter import ttk,messagebox
from fonction import listing_port, connecter
import serial

# https://tkdocs.com/tutorial/index.html
# https://docs.python.org/3/library/tkinter.ttk.html#widget

def script_bouton() :
    
    port = combobox_port.get()
    baudrate = combobox_baudrate.get()
    timeout = combobox_timeout.get()

    if connecter(port, baudrate, timeout) == True :
        combobox_port["state"] = "disabled"
        combobox_baudrate["state"] = "disabled"
        combobox_timeout["state"] = "disabled"
        bouton_connecter["state"] = "disabled"
        connexion.geometry("330x170")
    else : 
        messagebox.showwarning(title= "Erreur",
                               message= "Le port n'est pas ouvert")
        
connexion = Tk()
connexion.geometry("165x170")
connexion.resizable(False, False)
connexion.title("Parking")

port_disponible = listing_port()
combobox_port = ttk.Combobox(connexion, values = port_disponible, state= "readonly")
if port_disponible != [] : 
    combobox_port.set(port_disponible[0])
combobox_port.grid(row=0, column=0, padx=10, pady=10)

baudrate_disponible = ["4800", "9600", "19200" ]
combobox_baudrate = ttk.Combobox(connexion, values = baudrate_disponible, state= "readonly")
combobox_baudrate.set(baudrate_disponible[0])
combobox_baudrate.grid(row=1, column=0, padx=10, pady=10)

timeout_disponible = ["0" , "1"]
combobox_timeout = ttk.Combobox(connexion, values = timeout_disponible, state= "readonly")
combobox_timeout.set(timeout_disponible[0])
combobox_timeout.grid(row=2, column=0, padx=10, pady=10)

bouton_connecter = ttk.Button(connexion, text="Connecter", command=script_bouton)
bouton_connecter.grid(row=3, column=0, padx=10, pady=10)

connexion.update()
connexion.mainloop()