from tkinter import LabelFrame, Listbox, Label, Entry, Button, Variable
from .application import *
from utils import *

class Configuration_SP3(LabelFrame):

    def __init__(self, parent, dict_des_objets : dict[str, dict[str, str | int | bool | None]], liste_des_instances_appareil : list[SP3], listbox : Listbox ):
        super().__init__(parent, text= "Configuration du SP3")

        self.listbox: Listbox = listbox
        self.dict_des_objets: dict[str, dict[str, str | int | bool | None]] = dict_des_objets
        self.liste_des_instances_appareil: list[SP3] = liste_des_instances_appareil
        adresse_objet: str = self.listbox.selection_get()

        # Port
        label_port_com = Label(self, text= "Port COM de l'objet :")
        label_port_com.grid()

        afficher_port_com = Entry(self)
        afficher_port_com.insert(0, str(dict_des_objets[adresse_objet]["port"]))
        afficher_port_com.grid(padx= 10)
        afficher_port_com["state"] = "disabled"

        # Modele
        label_modele_objet = Label(self, text= "Modele de l'objet :")
        label_modele_objet.grid()

        afficher_modele_objet = Entry(self)
        afficher_modele_objet.insert(0, str(dict_des_objets[adresse_objet]["modele"]))
        afficher_modele_objet.grid()
        afficher_modele_objet["state"] = "disabled"

        # Version
        label_version_objet = Label(self, text= "Version logiciel de l'objet :")
        label_version_objet.grid()

        afficher_version_objet = Entry(self)
        afficher_version_objet.insert(0, str(dict_des_objets[adresse_objet]["version"]))
        afficher_version_objet.grid()
        afficher_version_objet["state"] = "disabled"

        # Adresse
        label_adresse_objet = Label(self, text= "Adresse de l'objet :")
        label_adresse_objet.grid()

        afficher_adresse_objet = Entry(self)
        afficher_adresse_objet.insert(0, adresse_objet)
        afficher_adresse_objet.grid()
        afficher_adresse_objet["state"] = "disabled"

        # Bouton fonction 01
        mode_test = Button(self, text="Activer Mode Test", command=self.ajout_fonction0x01)
        mode_test.grid(column= 1, row= 0, padx= 5, pady= 5)

        # Bouton fonction 02
        mode_calib = Button(self, text="Activer Mode Calibration", command=self.ajout_fonction0x02)
        mode_calib.grid(column= 1, row= 1, padx= 5, pady= 5)

        # Fonction 04
        self.valeur_potentiometre = Variable(self, value=dict_des_objets[adresse_objet]["valeur_potentiometre"] ,name="valeur_potentiometre")
        _valeur_potentiometre = Entry(self,textvariable=self.valeur_potentiometre)
        _valeur_potentiometre.grid(column= 1, row= 2, padx= 5, pady= 5)
        mode_calib = Button(self, text="Envoyer", command=self.ajout_fonction0x02)
        mode_calib.grid(column= 1, row= 3, padx= 5, pady= 5)


    def selection_appareil_listbox(self)  -> SP3:

        index: int = self.listbox.curselection()[0]
        appareil: SP3 = self.liste_des_instances_appareil[index]

        return appareil

    def ajout_fonction0x01(self):

        appareil = self.selection_appareil_listbox()
        appareil.mode_test()

    def ajout_fonction0x02(self) :

        appareil = self.selection_appareil_listbox()
        appareil.calibration_potentiomètre()

    def ajout_fonction0x04(self):
        
        appareil = self.selection_appareil_listbox()
        appareil.potentiometre = self.valeur_potentiometre