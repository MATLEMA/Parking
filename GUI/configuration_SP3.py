from tkinter import LabelFrame, Listbox, Label, Entry, Button, Variable, Frame, Canvas
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

        #-----------------------------------------------------------------------------------------#
        # Bouton fonction 01
        mode_test = Button(config_defaut, text="Activer Mode Test", command=self.ajout_fonction0x01)
        mode_test.grid(row= 8, padx= 5, pady= 5)

        #-----------------------------------------------------------------------------------------#
        potentiometreIO = LabelFrame(self, text= "Potentiomètre" )
        potentiometreIO.pack(side="left", anchor="nw")
        # Bouton fonction 02
        mode_calib_auto = Button(potentiometreIO, text="Activer Mode Calibration auto", command=self.ajout_fonction0x02)
        mode_calib_auto.grid(row= 0, padx= 5, pady= 5)

        # Fonctions 04 et 14
        self.valeur_potentiometre = Variable(potentiometreIO, value=dict_des_objets[self.adresse_objet]["valeur_potentiometre"] ,name="valeur_potentiometre")
        _valeur_potentiometre = Entry(potentiometreIO,textvariable=self.valeur_potentiometre)
        _valeur_potentiometre.grid(row= 1, padx= 5, pady= 5)
        mode_calib = Button(potentiometreIO, text="Envoyer", command=self.ajout_fonction0x04)
        mode_calib.grid(row= 2, padx= 5, pady= 5)

        #-----------------------------------------------------------------------------------------#
        maxdistanceIO = LabelFrame(self, text= "Distance maximal")
        maxdistanceIO.pack(side="left", anchor="nw")

        # Fonctions 06 et 11
        self.valeur_distance_maximal = Variable(maxdistanceIO, value= dict_des_objets[self.adresse_objet]["valeur_distance_maximal"] ,name="valeur_distance_maximal")
        _valeur_distance_maximal = Entry(maxdistanceIO, textvariable= self.valeur_distance_maximal)
        _valeur_distance_maximal.grid(row= 0, padx= 5, pady= 5)
        return_val_dist_max = Button(maxdistanceIO, text="Envoyer", command=self.ajout_fonction0x06)
        return_val_dist_max.grid(row= 1, padx= 5, pady= 5)

        #-----------------------------------------------------------------------------------------#
        mode_detection = LabelFrame(self, text= "Mode de détection")
        mode_detection.pack(side="left", anchor="nw")

        # Fonctions 06 et 11
        self.mode_de_detection = Variable(mode_detection, value= "vrai" if dict_des_objets[self.adresse_objet]["mode_detection"] == True else "faux" ,name="mode_detection")
        _mode_de_detection = Entry(mode_detection, textvariable= self.mode_de_detection)
        _mode_de_detection.grid(row= 1, padx= 5, pady= 5)
        return_mode_detection = Button(mode_detection, text="Envoyer", command=self.ajout_fonction0x07)
        return_mode_detection.grid(row= 2, padx= 5, pady= 5)

        #-----------------------------------------------------------------------------------------#
        
        mode_transceiver = LabelFrame(self, text= "Mode transceiver")
        mode_transceiver.pack(side="left", anchor="nw")

        self.mode_de_transceiver = Variable(mode_transceiver, value= "vrai" if dict_des_objets[self.adresse_objet]["mode_transceiver"] == True else "faux" ,name="mode_transceiver")
        _mode_de_transceiver = Entry(mode_transceiver, textvariable= self.mode_de_transceiver)
        _mode_de_transceiver.grid(row= 0, padx= 5, pady= 5)
        return_mode_transeiver = Button(mode_transceiver, text="Envoyer", command=self.ajout_fonction0x03)
        return_mode_transeiver.grid(row= 1, padx= 5, pady= 5)

        self.isplace_libre = LabelFrame(self, text= "Place libre")
        self.isplace_libre.pack(side="left", anchor="nw")

        self.indicateur = Canvas(self.isplace_libre, width= 50, height=50)
        self.indicateur.pack()
        self.cercle = self.indicateur.create_oval(5, 5, 45, 45)

        self.thread = threading.Thread(target=self.place_libre_thread)
        self.thread.start()

    def ajout_fonction0x01(self):

        self.appareil.mode_test()

    def ajout_fonction0x02(self) :

        self.appareil.calibration_potentiomètre()
        self.valeur_potentiometre.set(self.appareil.potentiometre)

    def ajout_fonction0x04(self):
        
        self.appareil.potentiometre = str(self.valeur_potentiometre.get())
        self.valeur_potentiometre.set(self.appareil.potentiometre)

    def ajout_fonction0x06(self):

        self.appareil.distance_maximal = str(self.valeur_distance_maximal.get())
        self.valeur_distance_maximal.set(self.appareil.distance_maximal)

    def ajout_fonction0x07(self):

        if self.mode_de_detection.get() == "vrai" :
            self.appareil.mode_detection = True
            self.mode_de_detection.set(True)
        else :
            self.appareil.mode_detection = False
            self.mode_de_detection.set(False)

    def ajout_fonction0x03(self):

        if self.mode_de_transceiver.get() == "vrai" :
            self.appareil.mode_transceiver = True
            self.mode_de_transceiver.set(True)
        else :
            self.appareil.mode_transceiver = False
            self.mode_de_transceiver.set(False)

    def place_libre_thread(self):

        while True:
            if self.appareil.place_libre():
                self.indicateur.itemconfig(self.cercle, fill= "green")
            else:
                self.indicateur.itemconfig(self.cercle, fill= "red")

            sleep(2)