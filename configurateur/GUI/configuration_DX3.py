from tkinter import LabelFrame, Listbox, Label, Entry, Button, Variable, Frame, Radiobutton, StringVar, ttk
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

        afficheur_labelframe = LabelFrame(self, text="Afficheur")
        afficheur_labelframe.pack(side="left", anchor="nw")

        # Fonction 40
        numero_variable = Variable(afficheur_labelframe, value="000")
        option_numero: list[str]= ["{0:0>3}".format(i) for i in range(0, 1000)]
        self.numero_entry = ttk.Combobox(afficheur_labelframe, textvariable=numero_variable, values=option_numero)
        numero_variable.set("000")
        self.numero_entry.grid(row=0, column=1, padx= 5, pady= 5)
        numero_bouton_envoyer = Button(afficheur_labelframe, text="Envoyer", command=self.modifie_afficheur)
        numero_bouton_envoyer.grid(row=1, column=1, padx= 5, pady= 5)

        # Fonction 4A et 4B
        self.parking_plein_variable = Variable(afficheur_labelframe)
        self.retourne_parking_plein()
        option_parking_plein: list[str]= ["Croix rouge", "Flèche rouge", "Full", "HEt"]
        self.parking_plein_combobox = ttk.Combobox(afficheur_labelframe, textvariable=self.parking_plein_variable, values=option_parking_plein)
        self.parking_plein_combobox.grid(row=0)
        parking_plein_envoyer = Button(afficheur_labelframe, text="Envoyer", command=self.modifie_parking_plein)
        parking_plein_envoyer.grid(row=1)

        # Fonction 48 et 49
        self.sens_variable = Variable(afficheur_labelframe)
        self.retourne_sens()
        option_sens: list[str]= ["< XXX", "XXX >"]
        self.sens_combobox= ttk.Combobox(afficheur_labelframe, textvariable=self.sens_variable, values=option_sens)
        self.sens_combobox.grid(row=2, column=0)
        sens_envoyer= Button(afficheur_labelframe, text="Envoyer", command=self.modifie_sens)
        sens_envoyer.grid(row=3, column=0)

    def modifie_afficheur(self) -> None:

        valeur: str = self.numero_entry.get()

        if len(valeur) > 3:
            self.numero_entry.delete(3, "end")
            
        self.appareil.afficheur(valeur)

    def modifie_parking_plein(self) -> None:
        
        valeur: str = self.parking_plein_combobox.get()

        match valeur:
            case "Croix rouge":
                self.appareil.parking_plein = "41"
            case "Flèche rouge":
                self.appareil.parking_plein = "43"
            case "Full":
                self.appareil.parking_plein = "80"
            case "HEt":
                self.appareil.parking_plein = "81"
        self.retourne_parking_plein()

    def retourne_parking_plein(self):
        try :
            valeur: str = self.appareil.parking_plein
        except:
            self.parking_plein_variable.set("N/A")
        else:
            match valeur:
                case "41":
                    self.parking_plein_variable.set("Croix rouge")
                case "43":
                    self.parking_plein_variable.set("Flèche rouge")
                case "80":
                    self.parking_plein_variable.set("Full")
                case "81":
                    self.parking_plein_variable.set("HEt")

    def modifie_sens(self) -> None:

        valeur: str = self.sens_combobox.get()
        if valeur == "< XXX":
            self.appareil.sens_afficheur= "01"
        else:
            self.appareil.sens_afficheur= "00"

        self.retourne_parking_plein()

    def retourne_sens(self) -> None:

        try:
            valeur: str = self.appareil.sens_afficheur
        except:
            self.sens_variable.set("N/A")
        else:
            if valeur == "01":
                self.sens_variable.set("< XXX")
            else:
                self.sens_variable.set("XXX >")