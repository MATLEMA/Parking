from tkinter import LabelFrame, Listbox, Label, Entry, Button, Variable
from .application import *
from utils import *

class Configuration_SP3(LabelFrame):

    def __init__(self, parent, dict_des_objets : dict[str, dict[str, str | int | bool | None]], liste_des_instances_appareil : list[SP3], listbox : Listbox ):
        super().__init__(parent, text= "Configuration du SP3")

        self.listbox: Listbox = listbox
        self.dict_des_objets: dict[str, dict[str, str | int | bool | None]] = dict_des_objets
        self.liste_des_instances_appareil: list[SP3] = liste_des_instances_appareil
        self.adresse_objet: str = self.listbox.selection_get()
        index: int = self.listbox.curselection()[0]
        self.appareil: SP3 = self.liste_des_instances_appareil[index]

        # Port
        label_port_com = Label(self, text= "Port COM de l'objet :")
        label_port_com.grid(column=0, row= 0)

        afficher_port_com = Entry(self)
        afficher_port_com.insert(0, str(dict_des_objets[self.adresse_objet]["port"]))
        afficher_port_com.grid(padx= 10, column= 0, row= 1)
        afficher_port_com["state"] = "disabled"

        # Modele
        label_modele_objet = Label(self, text= "Modele de l'objet :")
        label_modele_objet.grid(column= 0, row= 2)

        afficher_modele_objet = Entry(self)
        afficher_modele_objet.insert(0, str(dict_des_objets[self.adresse_objet]["modele"]))
        afficher_modele_objet.grid(column= 0, row= 3)
        afficher_modele_objet["state"] = "disabled"

        # Version
        label_version_objet = Label(self, text= "Version logiciel de l'objet :")
        label_version_objet.grid(column= 0, row= 4)

        afficher_version_objet = Entry(self)
        afficher_version_objet.insert(0, str(dict_des_objets[self.adresse_objet]["version"]))
        afficher_version_objet.grid(column=0, row=5)
        afficher_version_objet["state"] = "disabled"

        # Adresse
        label_adresse_objet = Label(self, text= "Adresse de l'objet :")
        label_adresse_objet.grid(column= 0, row= 6)

        afficher_adresse_objet = Entry(self)
        afficher_adresse_objet.insert(0, self.adresse_objet)
        afficher_adresse_objet.grid(column= 0, row= 7)
        afficher_adresse_objet["state"] = "disabled"

        # Bouton fonction 01
        mode_test = Button(self, text="Activer Mode Test", command=self.ajout_fonction0x01)
        mode_test.grid(column= 0, row= 8, padx= 5, pady= 5)


        potentiometreIO = LabelFrame(self, text= "Potentiomètre" )
        potentiometreIO.grid(column= 1, row=0, rowspan= 6)
        # Bouton fonction 02
        mode_calib_auto = Button(potentiometreIO, text="Activer Mode Calibration auto", command=self.ajout_fonction0x02)
        mode_calib_auto.grid(column= 1, row= 1, padx= 5, pady= 5)

        # Fonctions 04 et 14
        self.valeur_potentiometre = Variable(potentiometreIO, value=dict_des_objets[self.adresse_objet]["valeur_potentiometre"] ,name="valeur_potentiometre")
        _valeur_potentiometre = Entry(potentiometreIO,textvariable=self.valeur_potentiometre)
        _valeur_potentiometre.grid(column= 1, row= 2, padx= 5, pady= 5)
        mode_calib = Button(potentiometreIO, text="Envoyer", command=self.ajout_fonction0x04)
        mode_calib.grid(column= 1, row= 3, padx= 5, pady= 5)

    def ajout_fonction0x01(self):

        self.appareil.mode_test()

    def ajout_fonction0x02(self) :

        self.appareil.calibration_potentiomètre()
        self.valeur_potentiometre.set(self.appareil.potentiometre)

    def ajout_fonction0x04(self):
        
        self.appareil.potentiometre = str(self.valeur_potentiometre.get())
        self.valeur_potentiometre.set(self.appareil.potentiometre)