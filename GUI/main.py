from tkinter import Tk

from .connexion import Connexion
from .configuration import Configuration
from .configuration_objet import Configuration_SP3
from .recadrage_fenetre import centrer_fenetre

longeur = 185
largeur = 165

class Main:
    def __init__(self) -> None:

        parent = Tk()
        self.parent = parent

        centrer_fenetre(parent, largeur, longeur)

        parent.resizable(False, False)
        parent.title("Parking")

        self.fenetre_connexion = Connexion(parent, self.configuration, self.fermer_configuration)
        self.fenetre_connexion.pack(side="left", anchor= "nw")
    
        parent.mainloop()

    def configuration(self, port_actuelle) :

        self.application_configuration = Configuration(self.parent, port_actuelle, self.configuration_objet, self.fermer_configuration_objet)
        self.application_configuration.pack(side="left", expand=False, fill= "y",anchor= "n", ipady= 50, ipadx= 50)


    def fermer_configuration(self):

        self.application_configuration.destroy()

    def configuration_objet(self, dict_des_objets, liste_des_instances_appareil, listbox) :

        self.configuration_objet_SP3 = Configuration_SP3(self.parent, dict_des_objets, liste_des_instances_appareil, listbox)
        self.configuration_objet_SP3.pack(side="left", anchor="n")

    def fermer_configuration_objet(self, existe : bool) :

        if existe:
            self.configuration_objet_SP3.destroy()