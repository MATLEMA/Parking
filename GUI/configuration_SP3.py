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

        # Fenetre de configuration par défaut

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
        mode_test = Button(config_defaut, text="Activer Mode Test", command=self.si_detection_sol)
        mode_test.grid(row= 8, padx= 5, pady= 5)

        #-----------------------------------------------------------------------------------------#
        potentiometre_labelframe = LabelFrame(self, text= "Potentiomètre" )
        potentiometre_labelframe.pack(side="left", anchor="nw")
        # Bouton fonction 02
        mode_calib_auto_bouton = Button(potentiometre_labelframe, text="Activer Mode Calibration auto", command=self.toggle_calibration_auto)
        mode_calib_auto_bouton.grid(row= 0, padx= 5, pady= 5)

        # Fonctions 04 et 14
        self.valeur_potentiometre_variable = Variable(potentiometre_labelframe, value=dict_des_objets[self.adresse_objet]["valeur_potentiometre"] ,name="valeur_potentiometre")
        valeur_potentiometre_entry = Entry(potentiometre_labelframe,textvariable=self.valeur_potentiometre_variable)
        valeur_potentiometre_entry.grid(row= 1, padx= 5, pady= 5)
        mode_calib_bouton_envoyer = Button(potentiometre_labelframe, text="Envoyer", command=self.modifie_valeur_potentiometre)
        mode_calib_bouton_envoyer.grid(row= 2, padx= 5, pady= 5)
        mode_calib_bouton_recevoir = Button(potentiometre_labelframe, text="Recevoir", command=self.retourne_valeur_potentiometre)
        mode_calib_bouton_recevoir.grid(row= 3, padx= 5, pady= 5)

        #-----------------------------------------------------------------------------------------#
        maxdistance_labelframe = LabelFrame(self, text= "Distance maximal")
        maxdistance_labelframe.pack(side="left", anchor="nw")

        # Fonctions 06 et 11
        self.valeur_distance_maximal_variable = Variable(maxdistance_labelframe, value= dict_des_objets[self.adresse_objet]["valeur_distance_maximal"] ,name="valeur_distance_maximal")
        valeur_distance_maximal_entry = Entry(maxdistance_labelframe, textvariable= self.valeur_distance_maximal_variable)
        valeur_distance_maximal_entry.grid(row= 0, padx= 5, pady= 5)
        valeur_distance_maximal_bouton_envoyer = Button(maxdistance_labelframe, text="Envoyer", command=self.modifie_valeur_distance_maximal)
        valeur_distance_maximal_bouton_envoyer.grid(row= 1, padx= 5, pady= 5)
        valeur_distance_maximal_bouton_recevoir = Button(maxdistance_labelframe, text="Recevoir", command=self.retourne_valeur_distance_maximal)
        valeur_distance_maximal_bouton_recevoir.grid(row= 2, padx= 5, pady= 5)

        #-----------------------------------------------------------------------------------------#
        mode_detection_labelframe = LabelFrame(self, text= "Mode de détection")
        mode_detection_labelframe.pack(side="left", anchor="nw")

        # Fonctions 06 et 11
        self.mode_de_detection_variable = Variable(mode_detection_labelframe, value= "vrai" if dict_des_objets[self.adresse_objet]["mode_detection"] == True else "faux" ,name="mode_detection")
        mode_de_detection_entry = Entry(mode_detection_labelframe, textvariable= self.mode_de_detection_variable)
        mode_de_detection_entry.grid(row= 1, padx= 5, pady= 5)
        mode_detection_bouton_envoyer = Button(mode_detection_labelframe, text="Envoyer", command=self.modifie_prise_en_compte_detection_sol)
        mode_detection_bouton_envoyer.grid(row= 2, padx= 5, pady= 5)
        mode_detection_recevoir = Button(mode_detection_labelframe, text="Recevoir", command=self.retourne_prise_en_compte_detection_sol)
        mode_detection_recevoir.grid(row= 3, padx= 5, pady= 5)

        #-----------------------------------------------------------------------------------------#
        
        mode_transceiver_labelframe = LabelFrame(self, text= "Mode transceiver")
        mode_transceiver_labelframe.pack(side="left", anchor="nw")

        self.mode_de_transceiver_variable = Variable(mode_transceiver_labelframe, value= "vrai" if dict_des_objets[self.adresse_objet]["mode_transceiver"] == True else "faux" ,name="mode_transceiver")
        mode_de_transceiver_entry = Entry(mode_transceiver_labelframe, textvariable= self.mode_de_transceiver_variable)
        mode_de_transceiver_entry.grid(row= 0, padx= 5, pady= 5)
        mode_transeiver_bouton_envoyer = Button(mode_transceiver_labelframe, text="Envoyer", command=self.modifie_transceiver)
        mode_transeiver_bouton_envoyer.grid(row= 1, padx= 5, pady= 5)
        mode_transeiver_bouton_recevoir = Button(mode_transceiver_labelframe, text="Recevoir", command=self.retourne_transceiver)
        mode_transeiver_bouton_recevoir.grid(row= 2, padx= 5, pady= 5)

        self.isplace_libre = LabelFrame(self, text= "Place libre")
        self.isplace_libre.pack(side="left", anchor="nw")

        self.indicateur_place_libre = Canvas(self.isplace_libre, width= 50, height=50)
        self.indicateur_place_libre.pack()
        self.cercle_place_libre = self.indicateur_place_libre.create_oval(5, 5, 45, 45)

        self.thread_place_libre = threading.Thread(target=self.place_libre_thread)
        self.thread_place_libre.start()

    def si_detection_sol(self):

        self.appareil.mode_test()

    def toggle_calibration_auto(self) :

        self.appareil.calibration_potentiomètre()
        self.valeur_potentiometre_variable.set(self.appareil.potentiometre)

    def modifie_valeur_potentiometre(self):
        
        self.appareil.potentiometre = self.valeur_potentiometre_variable.get()
        self.valeur_potentiometre_variable.set(self.appareil.potentiometre)
    
    def retourne_valeur_potentiometre(self):

        try :
            valeur_potentiometre_variable = self.appareil.potentiometre
        except :
            self.valeur_potentiometre_variable.set("N/A")
        else :
            self.valeur_potentiometre_variable.set(valeur_potentiometre_variable)

    def modifie_valeur_distance_maximal(self):

        self.appareil.distance_maximal = self.valeur_distance_maximal_variable.get()
        self.valeur_distance_maximal_variable.set(self.appareil.distance_maximal)

    def retourne_valeur_distance_maximal(self):

        try :
            distance_maximal = self.appareil.distance_maximal
        except :
            self.valeur_distance_maximal_variable.set("N/A")
        else :
            self.valeur_distance_maximal_variable.set(distance_maximal)

    def modifie_prise_en_compte_detection_sol(self):

        mode = self.mode_de_detection_variable.get() 
        if mode in ["vrai","Vrai","v","V","true","True","t","T"] :
            self.appareil.mode_detection = True
            self.mode_de_detection_variable.set(True)
        elif mode in ["faux","Faux","f","F","false","False"] :
            self.appareil.mode_detection = False
            self.mode_de_detection_variable.set(False)
        else :
            raise SyntaxError("Invalide veuillez saisir faux/vrai")


    def retourne_prise_en_compte_detection_sol(self):
        
        try : 
            mode = self.appareil.mode_detection
        except :
            self.mode_de_detection_variable.set("N/A")
        else :
            if mode == True :
                self.mode_de_detection_variable.set("vrai")
            else:
                self.mode_de_detection_variable.set("faux")

    def modifie_transceiver(self):

        mode = self.mode_de_transceiver_variable.get()
        if mode in ["vrai","Vrai","v","V","true","True","t","T"] :
            self.appareil.transceiver = True
            self.mode_de_transceiver_variable.set(True)
        elif mode in ["faux","Faux","f","F","false","False"] :
            self.appareil.transceiver = False
            self.mode_de_transceiver_variable.set(False)
        else :
            raise SyntaxError("Invalide veuillez saisir faux/vrai")
        
    def retourne_transceiver(self):

        try : 
            mode = self.appareil.transceiver
        except :
            self.mode_de_transceiver_variable.set("N/A")
        else :
            if mode == True :
                self.mode_de_transceiver_variable.set("vrai")
            else:
                self.mode_de_transceiver_variable.set("faux")

    def place_libre_thread(self):

        while True:
            if self.appareil.place_libre():
                self.indicateur_place_libre.itemconfig(self.cercle_place_libre, fill= "green")
            else:
                self.indicateur_place_libre.itemconfig(self.cercle_place_libre, fill= "red")
            sleep(2)