from tkinter import ttk,messagebox, Tk, Frame, Listbox
from fonction import listing_port, connecter, detection_appareil, thread
import serial
from threading import Thread

class Main(Tk) :
    def __init__(self) :

        # Il faut appeller super() pour pouvoir configurer le __init__ de Tk dans notre propre __init__
        super().__init__()

        # Configuration de la fenetre principale 
        self.geometry("163x165")        # x40 = 1 widget
        self.title("Parking")
        self.resizable(False, False)

        # Configuration de la "grille"
        self.columnconfigure(3)
        self.rowconfigure(3)

        # Appellation des widgets 

        self.listbox = None
        self.Connexion()

    def Connexion(self) :

        fenetre_connexion = Frame(self, background="")
        fenetre_connexion.grid(row=0, column=0)

        def script_bouton() :
    
            port = combobox_port.get()
            baudrate = combobox_baudrate.get()
            timeout = combobox_timeout.get()

            # Ceci est juste un test !!
            if connecter(port, baudrate, timeout) == True :
                combobox_port["state"] = "disabled"
                combobox_baudrate["state"] = "disabled"
                combobox_timeout["state"] = "disabled"
                bouton_connecter["state"] = "disabled"
                self.resizable(True, True)
                serial.Serial(port, int(baudrate), timeout= float(timeout))
                if self.listbox is None :
                    self.Creation_listbox()

            else : 
                messagebox.showwarning(title= "Erreur",
                                    message= "Le port n'est pas ouvert")
        
        port_disponible = listing_port()
        combobox_port = ttk.Combobox(fenetre_connexion, values = port_disponible, state= "readonly")
        if port_disponible != [] : 
            combobox_port.set(port_disponible[0])
        combobox_port.grid(row=0, column=0, padx=10, pady=10)

        baudrate_disponible = ["4800", "9600", "19200" ]
        combobox_baudrate = ttk.Combobox(fenetre_connexion, values = baudrate_disponible, state= "readonly")
        combobox_baudrate.set(baudrate_disponible[0])
        combobox_baudrate.grid(row=1, column=0, padx=10, pady=10)

        timeout_disponible = ["0" , "0.004", "1"]
        combobox_timeout = ttk.Combobox(fenetre_connexion, values = timeout_disponible, state= "readonly")
        combobox_timeout.set(timeout_disponible[0])
        combobox_timeout.grid(row=2, column=0, padx=10, pady=10)

        bouton_connecter = ttk.Button(fenetre_connexion, text="Connecter", command= script_bouton)
        bouton_connecter.grid(row=3, column=0, padx=10, pady=10)
    
    def Creation_listbox(self) :
        
        fenetre_listbox = Frame(self, background="blue")
        fenetre_listbox.grid(row=1, column= 1, rowspan= 5)
        liste_objet = Listbox(fenetre_listbox)
        liste_objet.grid(row=1, column= 0, rowspan=10)

if __name__ == "__main__":
    application = Main()
    application.mainloop()
