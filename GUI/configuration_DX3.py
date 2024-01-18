from tkinter import LabelFrame, Listbox, Label, Entry, Button
from .main import *
from utils import *

class Configuration_DX3(LabelFrame):

    def __init__(self, parent, dict_des_objets : dict[str, dict[str, str | int | bool | None]], liste_des_instances_appareil : list[SP3 | DX3], listbox : Listbox ):
        super().__init__(parent, text= "Configuration du DX3")

        self.listbox: Listbox = listbox
        self.dict_des_objets: dict[str, dict[str, str | int | bool | None]] = dict_des_objets
        self.liste_des_instances_appareil: list[SP3 | DX3] = liste_des_instances_appareil
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