from tkinter import ttk,messagebox, Tk, Listbox, LabelFrame, Variable
from fonction import listing_port, connecter
import serial
from ma_class import Appareil

class Configuration(Tk) :

    liste_des_objets : dict[str,list[str]] = {}

    def __init__(self,parent) :

        self.configuration = LabelFrame(parent, text= "Configuration")
        self.configuration.pack(side="left", expand=False, fill= "y",anchor= "n", ipady= 50, ipadx= 50)

        self.variable_pour_liste = Variable()
        liste = Listbox(self.configuration, listvariable= self.variable_pour_liste)
        liste.pack(side="left", expand=True, fill= "both")

    def ajout_liste(self, objet : Appareil) :
        
        self.liste_des_objets[objet.port_serial] = [objet.modele, objet.adresse, str(objet.version)]
        self.maj_listbox()

    def maj_listbox(self):

        self.variable_pour_liste.set(list(list(self.liste_des_objets.values())[0])[0])

    def changement_de_port(self) :

        self.liste_des_objets.clear
        

class Connexion(Tk) :
    
    def __init__(self, parent) :

        self.parent = parent
        self.fenetre_connexion = LabelFrame(self.parent, text= "Connexion Port COM")
        self.fenetre_connexion.pack(side="left", anchor= "nw")

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

class Main :
    def __init__(self) :
        root = Tk()

        root.geometry("400x400")
        root.resizable(False, False)
        root.title("Parking")
        
        # Appellation des widgets 
        self.application_connexion = Connexion(root)
        self.application_configuration = Configuration(root)

        root.mainloop()

if __name__ == "__main__":
    Main()
