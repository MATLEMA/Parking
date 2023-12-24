from tkinter import ttk,messagebox, Tk, Frame, Listbox, LabelFrame
from fonction import listing_port, connecter
import serial

class Configuration(Frame) :
    def __init__(self,parent) :
        super().__init__(parent)

        self.configuration = LabelFrame(parent, text= "Configuration")
        self.configuration.pack(side="left", expand=False, fill= "y",anchor= "n", ipady= 50, ipadx= 50)

        liste = Listbox(self.configuration)
        liste.pack(side="left", expand=True, fill= "both")

class Connexion(Frame) :
    
    ancienne_fenetre = None
    
    def __init__(self, parent) :
    
        self.parent = parent
        self.fenetre_connexion = LabelFrame(self.parent, text= "Connexion port COM")
        self.fenetre_connexion.pack(side="left", expand= False, anchor= "nw")

        port_disponible = listing_port()
        self.combobox_port = ttk.Combobox(self.fenetre_connexion, values = port_disponible, state= "readonly")
        if port_disponible != [] : 
            self.combobox_port.set(port_disponible[0])
        self.combobox_port.grid(row=0, column=0, padx=10, pady=10)

        baudrate_disponible = ["4800", "9600", "19200" ]
        self.combobox_baudrate = ttk.Combobox(self.fenetre_connexion, values = baudrate_disponible, state= "readonly")
        self.combobox_baudrate.set(baudrate_disponible[0])
        self.combobox_baudrate.grid(row=1, column=0, padx=10, pady=10)

        timeout_disponible = ["0" , "0.004", "1"]
        self.combobox_timeout = ttk.Combobox(self.fenetre_connexion, values = timeout_disponible, state= "readonly")
        self.combobox_timeout.set(timeout_disponible[0])
        self.combobox_timeout.grid(row=2, column=0, padx=10, pady=10)

        self.bouton_connecter = ttk.Button(self.fenetre_connexion, text="Connecter", command= self.script_bouton_connexion)
        self.bouton_connecter.grid(row=3, column=0, padx=10, pady=10)
        Configuration(self.parent)

    def script_bouton_connexion(self) :
        
        port = self.combobox_port.get()
        baudrate = self.combobox_baudrate.get()
        timeout = self.combobox_timeout.get()

        if connecter(port, baudrate, timeout) == True :
            self.combobox_port["state"] = "disabled"
            self.combobox_baudrate["state"] = "disabled"
            self.combobox_timeout["state"] = "disabled"
            serial.Serial(port, int(baudrate), timeout= float(timeout))
            self.deconnexion_bouton()
        else : 
            messagebox.showwarning(title= "Erreur",
                                    message= "Le port n'est pas ouvert")

    def deconnexion_bouton(self) :

        self.bouton_connecter = ttk.Button(self.fenetre_connexion, text="Deconnecter", command=self.script_bouton_deconnexion)
        self.bouton_connecter.grid(row=3, column=0, padx=10, pady=10)
    
    def script_bouton_deconnexion(self) :

        self.combobox_port["state"] = "enabled"
        self.combobox_baudrate["state"] = "enabled"
        self.combobox_timeout["state"] = "enabled"
        self.bouton_connecter = ttk.Button(self.fenetre_connexion, text="Connecter", command= self.script_bouton_connexion)
        self.bouton_connecter.grid(row=3, column=0, padx=10, pady=10)

class Main() :
    def __init__(self) :
        root = Tk()

        root.geometry("400x400")
        root.resizable(False, False)
        root.title("Parking")
        
        # Appellation des widgets 
        application = Connexion(root)

        root.mainloop()

if __name__ == "__main__":
    Main()
