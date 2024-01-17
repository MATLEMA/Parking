from tkinter import ttk,messagebox, Tk, Listbox, LabelFrame, Variable, Button, Entry, Label
from fonction import listing_port, connecter, detection_appareil, fonction0x05
from serial import Serial
from ma_class import Appareil, SP3, DX3
import threading


# Variables

is_connecter = False
longeur = 185
largeur = 165

def centrer_fenetre(parent, longeur_fenetre : int, hauteur_fenetre: int) :

    longueur_ecran_hote = parent.winfo_screenwidth()
    hauteur_ecran_hote = parent.winfo_screenheight()

    longueur_ecran_hote = (longueur_ecran_hote/2) - (longeur_fenetre/2)
    hauteur_ecran_hote = (hauteur_ecran_hote/2) - (hauteur_fenetre/2)

    parent.geometry( "%dx%d+%d+%d" % (longeur_fenetre, hauteur_fenetre, longueur_ecran_hote, hauteur_ecran_hote))

def redefinir_fenetre(parent, longeur_fenetre : int, hauteur_fenetre: int) : 

    parent.geometry(f"{longeur_fenetre}x{hauteur_fenetre}")

class Configuration_SP3(LabelFrame):

    def __init__(self, parent, dict_des_objets : dict[str,list[str]], liste_des_instances_appareil : list[Appareil], listbox : Listbox ):
        super().__init__(parent, text= "Configuration du SP3")

        self.listbox: Listbox = listbox
        self.dict_des_objets: dict[str, list[str]] = dict_des_objets
        self.liste_des_instances_appareil: list[Appareil | SP3 | DX3] = liste_des_instances_appareil
        port_objet: str = self.listbox.selection_get()

        # Port
        label_port_com = Label(self, text= "Port COM de l'objet :")
        label_port_com.grid()

        afficher_port_com = Entry(self)
        afficher_port_com.insert(0, dict_des_objets[port_objet][1])
        afficher_port_com.grid(padx= 10)
        afficher_port_com["state"] = "disabled"

        # Modele
        label_modele_objet = Label(self, text= "Modele de l'objet :")
        label_modele_objet.grid()

        afficher_modele_objet = Entry(self)
        afficher_modele_objet.insert(0, dict_des_objets[port_objet][0])
        afficher_modele_objet.grid()
        afficher_modele_objet["state"] = "disabled"

        # Version
        label_version_objet = Label(self, text= "Version logiciel de l'objet :")
        label_version_objet.grid()

        afficher_version_objet = Entry(self)
        afficher_version_objet.insert(0, dict_des_objets[port_objet][2])
        afficher_version_objet.grid()
        afficher_version_objet["state"] = "disabled"

        # Adresse
        label_adresse_objet = Label(self, text= "Adresse de l'objet :")
        label_adresse_objet.grid()

        afficher_adresse_objet = Entry(self)
        afficher_adresse_objet.insert(0, port_objet)
        afficher_adresse_objet.grid()
        afficher_adresse_objet["state"] = "disabled"

        # Bouton fonction 01
        mode_test = Button(self, text="Activer Mode Test", command=self.ajout_fonction0x01)
        mode_test.grid(column= 1, row= 0, padx= 5, pady= 5)


    def selection_appareil_listbox(self)  -> SP3:

        index: int = self.listbox.curselection()[0]
        appareil: SP3 = self.liste_des_instances_appareil[index]        # ?
        return appareil

    def ajout_fonction0x01(self):

        appareil = self.selection_appareil_listbox()
        appareil.mode_test()

    def ajout_fonction0x02(self) :

        appareil = self.selection_appareil_listbox()
        appareil.calibration_potentiomètre()

class Configuration(LabelFrame) :

    dict_des_objets : dict[str,list[str]] = {}
    liste_des_instances_appareil: list[Appareil] = []

    def __init__(self, parent, port : Serial, fonction_rappel_ouvrir, fonction_rappel_fermer ) :
        super().__init__(parent, text= "Configuration")

        self.fonction_rappel_ouvrir = fonction_rappel_ouvrir
        self.fonction_rappel_fermer = fonction_rappel_fermer
        self.existe = None
        self.port_actuelle = port
        self.parent = parent


        self.variable_pour_liste = Variable()
        self.liste = Listbox(self, listvariable= self.variable_pour_liste)
        self.liste.pack(side="top", expand=True, fill= "both")


        self.ajout_liste(self.ajout_de_methode_objet(Appareil("4F31", self.port_actuelle, "SP3", 1.0)))

        self.ajout_liste(self.ajout_de_methode_objet(Appareil("4F32", self.port_actuelle, "SP3", 1.0)))

        self.liste.bind("<<ListboxSelect>>", self.objet_selectionner)

        self.configuration_objet = LabelFrame(self.parent, text= "Configuration de l'objet :")
        self.configuration_objet.pack(side="left", expand=False, anchor="n")

        # Ajout manuel d'adresse objet 

        self.adresse_entree = Label(self, text= " Veuillez inscrire l'adresse de l'objet :")
        self.adresse_entree.pack(side= "top", pady= 5)

        self.entree = Entry(self)
        self.entree.pack(side= "top")
        
        self.bouton_test_adresse_manuel = Button(self, text="Ajouter", command= self.ajout_manuel_objet)
        self.bouton_test_adresse_manuel.pack(side= "top", pady= 5)
        
    def ajout_de_methode_objet(self, appareil : Appareil)  -> SP3 | DX3 | Appareil:

        if appareil.modele == "SP3" :
            appareil = SP3(appareil.adresse, appareil.port_serial, appareil.modele, appareil.version)
            return appareil
        
        if appareil.modele == "DX3" :
            appareil = DX3(appareil.adresse, appareil.port_serial, appareil.modele, appareil.version)
            return appareil
        else : return appareil
        
    def ajout_liste(self, objet : Appareil) :
        
        self.dict_des_objets[objet.adresse] = [objet.modele, objet.port_serial.port, str(objet.version)]
        self.liste_des_instances_appareil.append(objet)
        self.maj_listbox()

    def maj_listbox(self):

        self.variable_pour_liste.set(list(self.dict_des_objets.keys()))

    def objet_selectionner(self, event) :
        
        redefinir_fenetre(self.parent, 795, 400)

        self.fonction_rappel_fermer(self.existe)
        self.existe = True
        self.fonction_rappel_ouvrir(self.dict_des_objets, self.liste_des_instances_appareil, self.liste)

    def nouveau_port(self) : 

        self.fonction_rappel_fermer()
        self.configuration_objet.destroy()
    
    def ajout_manuel_objet(self) :
        
        adresse = self.entree.get()

        if len(adresse) == 4 or len(adresse) == 2 :

            try :
                int(adresse, 16)
                self.entree.delete(0, "end")
                is_valid = True
                    
            except ValueError :
                self.entree.delete(0, "end")
                messagebox.showerror(title= "Erreur", message= "Entrer une valeur valide : 2 ou 4 charactères en hexa")
                is_valid = False

            if is_valid == True :
                try :
                    nom_appareil, version_appareil, _ = fonction0x05(self.port_actuelle, str(adresse))
                    self.ajout_liste(objet= Appareil(adresse, self.port_actuelle, nom_appareil, version_appareil))

                except NameError:
                    messagebox.showerror(title= "Erreur", message= "L'appareil n'a pas répondu !")

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
            self.detection_automatique_appareils = threading.Thread(target=detection_appareil, args=(self.port_actuelle, self.stop_thread), daemon= True)
            self.detection_automatique_appareils.start()

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
        self.detection_automatique_appareils.join()
        self.port_actuelle.close()
        self.combobox_port["state"] = "enabled"
        self.combobox_baudrate["state"] = "enabled"
        self.combobox_timeout["state"] = "enabled"
        
        self.bouton_connecter = ttk.Button(self, text="Connecter", command= self.script_bouton_connexion)
        self.bouton_connecter.grid(row=3, column=0, padx=10, pady=10)

        redefinir_fenetre(self.parent, largeur, longeur)

        self.fonction_rappel_fermer()
        

class Main:
    def __init__(self) -> None:

        parent = Tk()
        self.parent = parent

        centrer_fenetre(parent, largeur, longeur)

        parent.resizable(False, False)
        parent.title("Parking")

        self.fenetre_connexion = Connexion(parent, self.configuration, self.fermer_configuration)
        self.fenetre_connexion.pack(side="left", anchor= "nw")
    
        parent.mainloop()

    def configuration(self, port_actuelle) :

        self.application_configuration = Configuration(self.parent, port_actuelle, self.configuration_objet, self.fermer_configuration_objet)
        self.application_configuration.pack(side="left", expand=False, fill= "y",anchor= "n", ipady= 50, ipadx= 50)


    def fermer_configuration(self):

        self.application_configuration.destroy()

    def configuration_objet(self, dict_des_objets, liste_des_instances_appareil, listbox) :

        self.configuration_objet_SP3 = Configuration_SP3(self.parent, dict_des_objets, liste_des_instances_appareil, listbox)
        self.configuration_objet_SP3.pack(side="left", anchor="n")

    def fermer_configuration_objet(self, existe : bool) :

        if existe:
            self.configuration_objet_SP3.destroy()