from tkinter import LabelFrame, Listbox, Entry, Label, Button, Variable, messagebox
from serial import Serial
from .application import *
from utils import *
from .recadrage_fenetre import redefinir_fenetre, centrer_fenetre
from pprint import pprint, pformat

class Configuration(LabelFrame) :


    def __init__(self, parent, port : Serial, ouvrir_fenetre_SP3, ouvrir_fenetre_DX3, fermer_fenetre_objets ) :
        super().__init__(parent, text= "Configuration")

        self.ouvrir_fenetre_SP3 = ouvrir_fenetre_SP3
        self.ouvrir_fenetre_DX3 = ouvrir_fenetre_DX3
        self.fermer_fenetre_objets = fermer_fenetre_objets
        self.port_actuelle: Serial = port
        self.parent = parent
        self.dict_des_objets : dict[str, dict[str, str | int | bool | None]] = {}
        self.liste_des_instances_appareil: list[SP3 | DX3] = []

        self.variable_pour_liste = Variable()
        self.liste = Listbox(self, listvariable= self.variable_pour_liste)
        self.liste.pack(side="top", expand=True, fill= "both")

        # Test
        self.ajout_objet(Appareil("4F31", self.port_actuelle, "SP3", 1.0))

        self.ajout_objet(Appareil("4E", self.port_actuelle, "DX3", 1.0))

        # Permet de "bind" la sélection dans la listebox avec une fonction ici la fonction permettant d'ouvrir une fenetre
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

    def ajout_manuel_objet(self)  -> None:
        
        adresse: str = self.entree.get()

        # print du dictionnaire des objets
        pprint(pformat(self.dict_des_objets))

        if len(adresse) == 4 or len(adresse) == 2 :

            # Test si l'adresse est en format hexadecimal, renvoie True, supprime la saisie
            try :
                int(adresse, 16)
                self.entree.delete(0, "end")
                is_valid = True
                    
            except ValueError :
                self.entree.delete(0, "end")
                messagebox.showerror(title= "Erreur", message= "Entrer une valeur valide : 2 ou 4 charactères en hexa")
                is_valid = False

            # Test si un appareil est derrière l'adresse donnée (si elle répond ou non)
            # Si oui, on créera une instance Appareil, puis un instance DX3 ou SP3 en fonction de son nom de modèle
            if is_valid == True :
                try :
                    nom_appareil, version_appareil = fonction0x05(self.port_actuelle, str(adresse))
                    appareil_verifie = Appareil(adresse, self.port_actuelle, nom_appareil, version_appareil)
                    self.ajout_objet(appareil_verifie)

                except NameError:
                    messagebox.showerror(title= "Erreur", message= "L'appareil n'a pas répondu !")

    def ajout_objet(self, appareil: Appareil)  -> None:

        objet: SP3 | DX3 = self.assignation_class_objet(appareil)

        if isinstance(objet, SP3) :
            self.ajout_listbox_SP3(objet)
            
        if isinstance(objet, DX3) :
            self.ajout_listbox_DX3(objet)

    def assignation_class_objet(self, appareil : Appareil)  -> SP3 | DX3:

        if appareil.modele == "SP3" :
            appareil = SP3(appareil.adresse, appareil.port_serial, appareil.modele, appareil.version)
            return appareil
        
        if appareil.modele == "DX3" :
            appareil = DX3(appareil.adresse, appareil.port_serial, appareil.modele, appareil.version)
            return appareil
        
        else : raise TypeError("L'appareil n'a pas de modèle reconnu")

        
    def ajout_listbox_SP3(self, objet : SP3 )  -> None:
        
        self.dict_des_objets[objet.adresse] = {
            "modele": objet.modele,
            "port" : objet.port_serial.port,
            "version" : str(objet.version),
            "valeur_potentiometre" : objet.valeur_potentiometre,
            "valeur_distance_maximal" : objet.valeur_distance_maximal,
            "mode_detection" : objet._mode_detection,
            "mode_transceiver" : objet.mode_transceiver,
            "place_libre" : objet._place_libre
            }
        self.liste_des_instances_appareil.append(objet)
        self.maj_listbox()

    def ajout_listbox_DX3(self, objet: DX3)  -> None:

        self.dict_des_objets[objet.adresse] = {
            "modele": objet.modele,
            "port" : objet.port_serial.port,
            "version" : str(objet.version),
            "valeur_fleche": objet.valeur_fleche,
            }
        self.liste_des_instances_appareil.append(objet)
        self.maj_listbox()

    def maj_listbox(self) -> None:

        self.variable_pour_liste.set(list(self.dict_des_objets.keys()))

    def selection_objet(self, event)  -> None:
        
        redefinir_fenetre(self.parent, 1600, 800)
        try :
            adresse_objet: str = self.liste.selection_get()
        except :
            return

        # correction d'un bug si nous selections quelque chose d'autre que dans la listebox cela active ce module 
        # alors si la selection n'est pas dans la liste nous passons
        if adresse_objet not in self.dict_des_objets.keys() :
            return

        self.fermer_fenetre_objets()

        if str(self.dict_des_objets[adresse_objet]["modele"]) == "SP3" :
            self.ouvrir_fenetre_SP3(self.dict_des_objets, self.liste_des_instances_appareil, self.liste)

        if str(self.dict_des_objets[adresse_objet]["modele"]) == "DX3" :
            self.ouvrir_fenetre_DX3(self.dict_des_objets, self.liste_des_instances_appareil, self.liste)