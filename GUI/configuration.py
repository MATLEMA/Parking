from tkinter import LabelFrame, Listbox, Entry, Label, Button, Variable, messagebox
from serial import Serial
from .main import *
from utils import *
from .recadrage_fenetre import redefinir_fenetre

class Configuration(LabelFrame) :

    dict_des_objets : dict[str,dict[str, str]] = {}
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


        self.ajout_liste_SP3(self.ajout_de_methode_objet(Appareil("4F31", self.port_actuelle, "SP3", 1.0)))

        self.ajout_liste_SP3(self.ajout_de_methode_objet(Appareil("4F32", self.port_actuelle, "SP3", 1.0)))

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
        
    def ajout_liste_SP3(self, objet : SP3 ) :
        
        self.dict_des_objets[objet.adresse] = {"modele": objet.modele, "port" : objet.port_serial.port, "version" : str(objet.version), "valeur potentiometre" : objet.valeur_potentiometre, "valeur_distance_maximal" : objet.valeur_distance_maximal, "mode_detection" : objet._mode_detection, "mode_transceiver" : objet.mode_transceiver, "place_libre" : objet._place_libre}
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

        print(self.dict_des_objets)

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
                    objet= self.ajout_de_methode_objet(Appareil(adresse, self.port_actuelle, nom_appareil, version_appareil))
                    if objet == SP3 :
                        self.ajout_liste_SP3(objet)

                except NameError:
                    messagebox.showerror(title= "Erreur", message= "L'appareil n'a pas répondu !")