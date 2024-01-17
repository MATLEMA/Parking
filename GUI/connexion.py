from utils import *
from tkinter import ttk, LabelFrame, messagebox
from .recadrage_fenetre import redefinir_fenetre

longeur = 185
largeur = 165

class Connexion(LabelFrame) :
    
    def __init__(self, parent, fonction_rappel_ouvrir, fonction_rappel_fermer) :
        super().__init__(parent , text= "Connexion")
        self.parent = parent
        self.fonction_rappel_ouvrir = fonction_rappel_ouvrir
        self.fonction_rappel_fermer = fonction_rappel_fermer

        port_disponible = listing_port()
        self.combobox_port = ttk.Combobox(self, values = port_disponible, state= "readonly")
        if port_disponible != [] : 
            self.combobox_port.set(port_disponible[0])
        self.combobox_port.grid(row=0, column=0, padx=10, pady=10)

        baudrate_disponible = ["4800", "9600", "19200" ]
        self.combobox_baudrate = ttk.Combobox(self, values = baudrate_disponible, state= "readonly")
        self.combobox_baudrate.set(baudrate_disponible[0])
        self.combobox_baudrate.grid(row=1, column=0, padx=10, pady=10)

        timeout_disponible = ["0" , "0.004", "1"]
        self.combobox_timeout = ttk.Combobox(self, values = timeout_disponible, state= "readonly")
        self.combobox_timeout.set(timeout_disponible[0])
        self.combobox_timeout.grid(row=2, column=0, padx=10, pady=10)

        self.bouton_connecter = ttk.Button(self, text="Connecter", command= self.script_bouton_connexion)
        self.bouton_connecter.grid(row=3, column=0, padx=10, pady=10)

    def script_bouton_connexion(self) :

        port = self.combobox_port.get()
        baudrate = self.combobox_baudrate.get()
        timeout = self.combobox_timeout.get()

        if connecter(port, baudrate, timeout) == True :
            
            self.port_actuelle = Serial(port, int(baudrate), timeout= float(timeout), write_timeout= 0)

            # Lancement du Thread pour la détection automatique des appareils

            self.stop_thread = threading.Event()
            """self.detection_automatique_appareils = threading.Thread(target=detection_appareil, args=(self.port_actuelle, self.stop_thread), daemon= True)
            self.detection_automatique_appareils.start() """

            self.combobox_port["state"] = "disabled"
            self.combobox_baudrate["state"] = "disabled"
            self.combobox_timeout["state"] = "disabled"

            redefinir_fenetre(self.parent, 395, 400)

            # Toutes les variables passées dans cette fonction seront envoyer dans la class configuration
            self.fonction_rappel_ouvrir(self.port_actuelle)

            self.deconnexion_bouton()
        else : 
            messagebox.showwarning(title= "Erreur",
                                    message= "Le port n'est pas ouvert")

    def deconnexion_bouton(self) :

        self.bouton_connecter = ttk.Button(self, text="Deconnecter", command=self.script_bouton_deconnexion)
        self.bouton_connecter.grid(row=3, column=0, padx=10, pady=10)
    
    def script_bouton_deconnexion(self) :

        self.stop_thread.set()
        "self.detection_automatique_appareils.join()"
        self.port_actuelle.close()
        self.combobox_port["state"] = "enabled"
        self.combobox_baudrate["state"] = "enabled"
        self.combobox_timeout["state"] = "enabled"
        
        self.bouton_connecter = ttk.Button(self, text="Connecter", command= self.script_bouton_connexion)
        self.bouton_connecter.grid(row=3, column=0, padx=10, pady=10)

        redefinir_fenetre(self.parent, largeur, longeur)

        self.fonction_rappel_fermer()