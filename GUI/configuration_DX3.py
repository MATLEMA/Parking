from tkinter import LabelFrame, Listbox, Label, Entry, Button, Variable, Frame, Radiobutton, StringVar
from .application import *
from utils import *

class Configuration_DX3(LabelFrame):

    def __init__(self, parent, dict_des_objets : dict[str, dict[str, str | int | bool | None]], liste_des_instances_appareil : list[DX3], listbox : Listbox ):
        super().__init__(parent, text= "Configuration du DX3")

        self.listbox: Listbox = listbox
        self.dict_des_objets: dict[str, dict[str, str | int | bool | None]] = dict_des_objets
        self.liste_des_instances_appareil: list[DX3] = liste_des_instances_appareil
        self.adresse_objet: str = self.listbox.selection_get()
        index: int = self.listbox.curselection()[0]
        self.appareil: DX3 = self.liste_des_instances_appareil[index]

        # Fenetre configuration par défaut

        config_defaut = Frame(self)
        config_defaut.pack(side="left", anchor="nw")
        # Port
        label_port_com = Label(config_defaut, text= "Port COM de l'objet :")
        label_port_com.grid(column=0, row= 0)

        afficher_port_com = Entry(config_defaut)
        afficher_port_com.insert(0, str(dict_des_objets[self.adresse_objet]["port"]))
        afficher_port_com.grid(padx= 10, column= 0, row= 1)
        afficher_port_com["state"] = "disabled"

        # Modele
        label_modele_objet = Label(config_defaut, text= "Modele de l'objet :")
        label_modele_objet.grid(column= 0, row= 2)

        afficher_modele_objet = Entry(config_defaut)
        afficher_modele_objet.insert(0, str(dict_des_objets[self.adresse_objet]["modele"]))
        afficher_modele_objet.grid(column= 0, row= 3)
        afficher_modele_objet["state"] = "disabled"

        # Version
        label_version_objet = Label(config_defaut, text= "Version logiciel de l'objet :")
        label_version_objet.grid(column= 0, row= 4)

        afficher_version_objet = Entry(config_defaut)
        afficher_version_objet.insert(0, str(dict_des_objets[self.adresse_objet]["version"]))
        afficher_version_objet.grid(column=0, row=5)
        afficher_version_objet["state"] = "disabled"

        # Adresse
        label_adresse_objet = Label(config_defaut, text= "Adresse de l'objet :")
        label_adresse_objet.grid(column= 0, row= 6)

        afficher_adresse_objet = Entry(config_defaut)
        afficher_adresse_objet.insert(0, self.adresse_objet)
        afficher_adresse_objet.grid(column= 0, row= 7)
        afficher_adresse_objet["state"] = "disabled"

        #-----------------------------------------------------------------------#

        fleche = LabelFrame(self, text= "Flèche")
        fleche.pack(side="left", anchor="nw")

        # Fonctions 4E et 4F
        self.fleche_variable = StringVar(value=dict_des_objets[self.adresse_objet]["valeur_fleche"]) # type: ignore
        f_haut_gauche = Radiobutton(fleche, text=u"\u2196", font=("Courier", 30), variable= self.fleche_variable, value="0A") 
        f_haut = Radiobutton(fleche, text=u"\u2191", font=("Courier", 30), variable= self.fleche_variable, value="02")
        f_haut_droite = Radiobutton(fleche, text=u"\u2197", font=("Courier", 30), variable= self.fleche_variable, value="07")
        f_gauche = Radiobutton(fleche, text=u"\u2190", font=("Courier", 30), variable= self.fleche_variable, value="03")
        f_droite = Radiobutton(fleche, text=u"\u2192", font=("Courier", 30), variable= self.fleche_variable, value="01")
        f_bas_gauche = Radiobutton(fleche, text=u"\u2199", font=("Courier", 30), variable= self.fleche_variable, value="09")
        f_bas = Radiobutton(fleche, text=u"\u2193", font=("Courier", 30), variable= self.fleche_variable, value="04")
        f_bas_droite = Radiobutton(fleche, text=u"\u2198", font=("Courier", 30), variable= self.fleche_variable, value="08")
        f_bas_vert_droite = Radiobutton(fleche, text=u"\u21B1", font=("Courier", 30), variable= self.fleche_variable, value="05")
        f_bas_vert_gauche = Radiobutton(fleche, text=u"\u21B0", font=("Courier", 30), variable= self.fleche_variable, value="06")

        f_haut_gauche.grid(column=0, row=0)
        f_haut.grid(column=1, row=0)
        f_haut_droite.grid(column=2, row=0)
        f_gauche.grid(column=0, row=1)
        f_droite.grid(column=2, row=1)
        f_bas_gauche.grid(column=0, row=2)
        f_bas.grid(column=1, row=2)
        f_bas_droite.grid(column=2, row=2)
        f_bas_vert_droite.grid(column=2, row=3)
        f_bas_vert_gauche.grid(column=0, row=3)

        bouton_envoyer_fleche = Button(fleche, text="Envoyer", command=self.modifie_fleche)
        bouton_envoyer_fleche.grid(column=1, row= 1, padx= 5, pady= 5)

    def modifie_fleche(self) -> None:

        hexa_fleche = self.fleche_variable.get()

        if hexa_fleche == "N/A":
            print("Incorrect")
            return
        
        self.appareil.fleche = hexa_fleche

        self.fleche_variable.set(self.appareil.fleche)
        
