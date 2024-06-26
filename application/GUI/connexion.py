from utils import *
from tkinter import ttk, LabelFrame, messagebox
from serial import Serial
from .recadrage_fenetre import redefinir_fenetre, centrer_fenetre

longeur = 185
largeur = 165
nouvelle_fenetre_longueur = 370
nouvelle_fenetre_hauteur = 300

class Connexion(LabelFrame) :
    
    def __init__(
            self,
            parent,
            ouvrir_gestion_DX3,
            fermer_gestion_DX3,
            fermer_gestion_SP3,
            ouvrir_parking,
            fermer_parking
            ) :
        super().__init__(parent , text= "Connexion")

        self.parent = parent
        self.ouvrir_gestion_DX3 = ouvrir_gestion_DX3
        self.fermer_gestion_DX3 = fermer_gestion_DX3
        self.fermer_gestion_SP3 = fermer_gestion_SP3
        self.ouvrir_parking = ouvrir_parking
        self.fermer_parking = fermer_parking

        # Listing des ports 
        port_disponible: list[str] = listing_port()
        self.combobox_port = ttk.Combobox(self, values = port_disponible, state= "readonly")
        if port_disponible != [] : 
            self.combobox_port.set(port_disponible[0])
        self.combobox_port.grid(row=0, column=0, padx=10, pady=10)

        # Listing des baudrates
        baudrate_disponible: list[str] = ["19200", "9600", "4800" ]
        self.combobox_baudrate = ttk.Combobox(self, values = baudrate_disponible, state= "readonly")
        self.combobox_baudrate.set(baudrate_disponible[0])
        self.combobox_baudrate.grid(row=1, column=0, padx=10, pady=10)

        # Listing des timeouts
        timeout_disponible: list[str] = ["0.030", "0", "0.004", "1"]
        self.combobox_timeout = ttk.Combobox(self, values = timeout_disponible, state= "readonly")
        self.combobox_timeout.set(timeout_disponible[0])
        self.combobox_timeout.grid(row=2, column=0, padx=10, pady=10)

        # Création du bouton connexion qui valide les saisies précédentes
        self.connexion_bouton()
        
    def connexion_bouton(self):

        self.bouton_connecter = ttk.Button(self, text="Connecter", command= self.script_bouton_connexion)
        self.bouton_connecter.grid(row=3, column=0, padx=10, pady=10)

    def deconnexion_bouton(self) :

        self.bouton_connecter = ttk.Button(self, text="Deconnecter", command=self.script_bouton_deconnexion)
        self.bouton_connecter.grid(row=3, column=0, padx=10, pady=10)

    def script_bouton_connexion(self) :

        port = self.combobox_port.get()
        baudrate = self.combobox_baudrate.get()
        timeout = self.combobox_timeout.get()

        # Test si le port sélectionné est valide (ouvert/fermé)
        if connecter(port, baudrate, timeout) == True :             # Try / except
            
            self.port_actuelle = Serial(port, int(baudrate), timeout= float(timeout), write_timeout= 0)

            self.combobox_port["state"] = "disabled"
            self.combobox_baudrate["state"] = "disabled"
            self.combobox_timeout["state"] = "disabled"

            centrer_fenetre(self.parent, nouvelle_fenetre_longueur, nouvelle_fenetre_hauteur)

            # Toutes les variables passées dans cette fonction seront envoyer dans la class configuration
            self.ouvrir_gestion_DX3(self.port_actuelle)

            self.deconnexion_bouton()

        else : 
            messagebox.showwarning(title= "Erreur",
                                   message= "Le port n'est pas ouvert")
    
    def script_bouton_deconnexion(self) :

        # Remise à zéro de l'application
        self.port_actuelle.close()
        self.combobox_port["state"] = "enabled"
        self.combobox_baudrate["state"] = "enabled"
        self.combobox_timeout["state"] = "enabled"
        
        self.bouton_connecter = ttk.Button(self, text="Connecter", command= self.script_bouton_connexion)
        self.bouton_connecter.grid(row=3, column=0, padx=10, pady=10)

        redefinir_fenetre(self.parent, largeur, longeur)
        
        self.fermer_gestion_DX3()
        self.fermer_gestion_SP3()
        self.fermer_parking()