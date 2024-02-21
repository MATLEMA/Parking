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

        fleche = LabelFrame(self, text= "Flèche")
        fleche.pack(side="left", anchor="nw")

        # Fonctions 4E et 4F
        self.fleche_variable = StringVar()
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

        fleche_bouton_envoyer = Button(fleche, text="Envoyer", command=self.modifie_fleche)
        fleche_bouton_envoyer.grid(column=1, row= 1, padx= 5, pady= 5)

        afficheur_labelframe = LabelFrame(self, text="Afficheur")
        afficheur_labelframe.pack(side="left", anchor="nw")

        # Fonction 40
        numero_variable = Variable(afficheur_labelframe, value="000")
        self.numero_entry = Entry(afficheur_labelframe, textvariable=numero_variable)
        self.numero_entry.grid(row=0)
        numero_bouton_envoyer = Button(afficheur_labelframe, text="Envoyer", command=self.modifie_afficheur)
        numero_bouton_envoyer.grid(row=1)

        # Fonction 4A et 4B
        self.parking_plein_variable = Variable(afficheur_labelframe)
        self.retourne_parking_plein()
        option_parking_plein: list[str]= ["Croix rouge", "Flèche rouge", "Full", "HEt"]
        self.parking_plein_combobox = ttk.Combobox(afficheur_labelframe, textvariable=self.parking_plein_variable, values=option_parking_plein)
        self.parking_plein_combobox.grid(row=0)
        parking_plein_envoyer = Button(afficheur_labelframe, text="Envoyer", command=self.modifie_parking_plein)
        parking_plein_envoyer.grid(row=1)

    def modifie_fleche(self) -> None:

        hexa_fleche = self.fleche_variable.get()

        if hexa_fleche == "N/A":
            return print("Incorrect")

        self.appareil.fleche = hexa_fleche
        self.fleche_variable.set(self.appareil.fleche)

    def retourne_fleche(self):

        try:
            self.fleche_variable.set(self.appareil.fleche)
        except:
            self.fleche_variable.set("N/A")

    def modifie_afficheur(self):

        valeur: str = self.numero_entry.get()

        if len(valeur) > 3:
            self.numero_entry.delete(3, "end")
            
        self.appareil.afficheur(valeur)

    def modifie_parking_plein(self):
        
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
        self.parking_plein_combobox.set(self.appareil.parking_plein)

    def retourne_parking_plein(self):
        try :
            self.parking_plein_variable.set(self.appareil.parking_plein)
        except:
            self.parking_plein_variable.set("N/A")
                
