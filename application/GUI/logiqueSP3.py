from serial import Serial
from tkinter import LabelFrame, Tk, Variable, Listbox, Button, Label, Entry, messagebox
from utils import Appareil, fonction0x05, SP3, DX3, Parking

class GestionListboxSP3(LabelFrame):

    def __init__(self, parent : Tk, port : Serial):
        super().__init__(parent, text= "SP3")
        
        self.port: Serial = port
        self.parent: Tk = parent
        self.liste_SP3: list[SP3] = []
        self.dict_des_objets: dict[str, dict[str, str | None | bool]] = {}

        self.variable_pour_liste = Variable()
        self.liste = Listbox(self, listvariable= self.variable_pour_liste)
        self.liste.pack(side="top", expand=True, fill= "both")

        # Permet de "bind" la sélection dans la listebox avec une fonction ici la fonction permettant d'ouvrir une fenetre
        ##### Pour l'implémentation de la suppression des items dans la listbox
        #self.liste.bind("<<ListboxSelect>>", self.selection_objet)

        # Ajout manuel d'adresse objet 

        self.adresse_entree = Label(self, text= " Veuillez inscrire l'adresse de l'objet :")
        self.adresse_entree.pack(side= "top", pady= 5)

        self.entree = Entry(self)
        self.entree.pack(side= "top")
        
        self.bouton_test_adresse_manuel = Button(self, text="Ajouter", command= self.ajout_manuel_objet)
        self.bouton_test_adresse_manuel.pack(side= "top", pady= 5)

    def ajout_manuel_objet(self)  -> None:
        
        adresse: str = self.entree.get()

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
            # Si oui, on créera une instance Appareil, puis un instance SP3 en fonction de son nom de modèle
            if is_valid == True :
                try :
                    nom_appareil, _ = fonction0x05(self.port, str(adresse))
                    appareil_verifie = Appareil(adresse, self.port, nom_appareil)
                    self.ajout_objet(appareil_verifie)

                except NameError:
                    messagebox.showerror(title= "Erreur", message= "L'appareil n'a pas répondu !")

    def ajout_objet(self, appareil: Appareil)  -> None:

        objet: SP3 = self.assignation_class_objet(appareil)

        if isinstance(objet, SP3) :
            self.ajout_listbox_SP3(objet)

    def assignation_class_objet(self, appareil : Appareil)  -> SP3:

        if appareil.modele == "SP3" :
            appareil = SP3(appareil.adresse, appareil.port_serial, appareil.modele)
            return appareil
        
        else : raise TypeError("L'appareil n'a pas de modèle reconnu")

        
    def ajout_listbox_SP3(self, objet : SP3 )  -> None:
        
        self.dict_des_objets.clear()

        self.dict_des_objets[objet.adresse] = {
            "modele": objet.modele,
            "port" : objet.port_serial.port,
            }

        self.liste_SP3.append(objet)

        self.maj_listbox()

    def maj_listbox(self) -> None:

        self.variable_pour_liste.set(list(self.dict_des_objets.keys()))

