from tkinter import *
from tkinter import ttk,messagebox, Tk
from fonction import listing_port, connecter
import serial
from time import sleep

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
        fenetre.geometry("330x190")
        fenetre.resizable(False, True)
        port_serial = serial.Serial(port, int(baudrate), timeout= float(timeout))
        liste_des_objets()
        return port_serial
    else : 
        messagebox.showwarning(title= "Erreur",
                               message= "Le port n'est pas ouvert")
        
def liste_des_objets() :
    def eee(event):
        fenetre.geometry("500x300")
        fenetre_boutons = Frame(fenetre)
        fenetre_boutons.grid(row= 0, column= 2, padx=10, pady=10)
        if liste.get(liste.curselection()) == "test0" :   
            for widget in fenetre_boutons.winfo_children():
                widget.destroy()
            r = Radiobutton(fenetre_boutons, text="test",)
            x = Radiobutton(fenetre_boutons, text="test")
            r.grid(row= 0, column= 0)
            x.grid(row= 1, column= 0)
        else : 
            for widget in fenetre_boutons.winfo_children():
                widget.destroy()
            o = Radiobutton(fenetre_boutons, text="test2",)
            i = Radiobutton(fenetre_boutons, text="test2")
            o.grid(row= 0, column= 0)
            i.grid(row=1, column= 0)
    liste = Listbox(connexion)
    liste.insert(1, "test0")
    liste.insert(2, "test2")
    liste.grid(row=0, column= 1, rowspan= 4)
    liste.bind("<<ListboxSelect>>", eee)


fenetre = Tk()
connexion = Frame(fenetre)
connexion.grid(row=0, column=0, padx=10, pady=10)
fenetre.geometry("180x175")
fenetre.resizable(False, False)
fenetre.title("Parking")

port_disponible = listing_port()
combobox_port = ttk.Combobox(connexion, values = port_disponible, state= "readonly")
if port_disponible != [] : 
    combobox_port.set(port_disponible[0])
combobox_port.grid(row=0, column=0, padx=10, pady=10)

baudrate_disponible = ["4800", "9600", "19200" ]
combobox_baudrate = ttk.Combobox(connexion, values = baudrate_disponible, state= "readonly")
combobox_baudrate.set(baudrate_disponible[0])
combobox_baudrate.grid(row=1, column=0, padx=10, pady=10)

timeout_disponible = ["0" , "0.004", "1"]
combobox_timeout = ttk.Combobox(connexion, values = timeout_disponible, state= "readonly")
combobox_timeout.set(timeout_disponible[0])
combobox_timeout.grid(row=2, column=0, padx=10, pady=10)

bouton_connecter = ttk.Button(connexion, text="Connecter", command=script_bouton)
bouton_connecter.grid(row=3, column=0, padx=10, pady=10)

connexion.update()
connexion.mainloop()