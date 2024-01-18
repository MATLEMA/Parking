from tkinter import LabelFrame, Listbox, Entry, Label, Button, Variable, messagebox
from serial import Serial
from .main import *
from utils import *
from .recadrage_fenetre import redefinir_fenetre
from pprint import pprint, pformat

class Configuration(LabelFrame) :

    dict_des_objets : dict[str, dict[str, str | int | bool | None]] = {}
    liste_des_instances_appareil: list[SP3 | DX3] = []

    def __init__(self, parent, port : Serial, ouvrir_fenetre_SP3, ouvrir_fenetre_DX3, fermer_fenetre_objet ) :
        super().__init__(parent, text= "Configuration")

        self.ouvrir_fenetre_SP3 = ouvrir_fenetre_SP3
        self.ouvrir_fenetre_DX3 = ouvrir_fenetre_DX3
        self.fermer_fenetre_objet = fermer_fenetre_objet
        self.existe = None
        self.port_actuelle = port
        self.parent = parent


        self.variable_pour_liste = Variable()
        self.liste = Listbox(self, listvariable= self.variable_pour_liste)
        self.liste.pack(side="top", expand=True, fill= "both")

        self.post_assignation_liste(self.assignation_class_objet(Appareil("4F31", self.port_actuelle, "SP3", 1.0)))

        self.post_assignation_liste(self.assignation_class_objet(Appareil("4F32", self.port_actuelle, "SP3", 1.0)))

        self.liste.bind("<<ListboxSelect>>", self.selection_objet)

        self.configuration_objet = LabelFrame(self.parent, text= "Configuration de l'objet :")
        self.configuration_objet.pack(side="left", expand=False, anchor="n")

        # Ajout manuel d'adresse objet 

        self.adresse_entree = Label(self, text= " Veuillez inscrire l'adresse de l'objet :")
        self.adresse_entree.pack(side= "top", pady= 5)

        self.entree = Entry(self)
        self.entree.pack(side= "top")
        
        self.bouton_test_adresse_manuel = Button(self, text="Ajouter", command= self.ajout_manuel_objet)
        self.bouton_test_adresse_manuel.pack(side= "top", pady= 5)
        
    def assignation_class_objet(self, appareil : Appareil)  -> SP3 | DX3:

        if appareil.modele == "SP3" :
            appareil = SP3(appareil.adresse, appareil.port_serial, appareil.modele, appareil.version)
            return appareil
        
        if appareil.modele == "DX3" :
            appareil = DX3(appareil.adresse, appareil.port_serial, appareil.modele, appareil.version)
            return appareil
        
        else : raise TypeError("L'appareil n'a pas de modèle reconnu")
        
    def ajout_listbox_SP3(self, objet : SP3 ) :
        
        self.dict_des_objets[objet.adresse] = {"modele": objet.modele, "port" : objet.port_serial.port, "version" : str(objet.version), "valeur potentiometre" : objet.valeur_potentiometre, "valeur_distance_maximal" : objet.valeur_distance_maximal, "mode_detection" : objet._mode_detection, "mode_transceiver" : objet.mode_transceiver, "place_libre" : objet._place_libre}
        self.liste_des_instances_appareil.append(objet)
        self.maj_listbox()

    def ajout_listbox_DX3(self, objet: DX3) :

        self.dict_des_objets[objet.adresse] = {"modele": objet.modele, "port" : objet.port_serial.port, "version" : str(objet.version)}
        self.liste_des_instances_appareil.append(objet)
        self.maj_listbox()

    def maj_listbox(self):

        self.variable_pour_liste.set(list(self.dict_des_objets.keys()))

    def selection_objet(self, event) :
        
        redefinir_fenetre(self.parent, 795, 400)
        adresse_objet: str = self.liste.selection_get()

        self.fermer_fenetre_objet()

        if str(self.dict_des_objets[adresse_objet]["modele"]) == "SP3" :
            self.ouvrir_fenetre_SP3(self.dict_des_objets, self.liste_des_instances_appareil, self.liste)

        if str(self.dict_des_objets[adresse_objet]["modele"]) == "DX3" :
            self.ouvrir_fenetre_DX3(self.dict_des_objets, self.liste_des_instances_appareil, self.liste)
    
    def ajout_manuel_objet(self) :
        
        adresse = self.entree.get()

        pprint(pformat(self.dict_des_objets))

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
                    # nom_appareil, version_appareil, _ = fonction0x05(self.port_actuelle, str(adresse))
                    nom_appareil = "DX3"
                    version_appareil = 1.3
                    appareil_verifie = Appareil(adresse, self.port_actuelle, nom_appareil, version_appareil)
                    self.post_assignation_liste(appareil_verifie)

                except NameError:
                    messagebox.showerror(title= "Erreur", message= "L'appareil n'a pas répondu !")

    def post_assignation_liste(self, appareil: Appareil) :

        objet: SP3 | DX3 = self.assignation_class_objet(appareil)

        if isinstance(objet, SP3) :
            self.ajout_listbox_SP3(objet)
            
        if isinstance(objet, DX3) :
            self.ajout_listbox_DX3(objet)