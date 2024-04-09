from tkinter import Tk

from .connexion import Connexion
from .configuration import Configuration
from .configuration_SP3 import Configuration_SP3
from .configuration_DX3 import Configuration_DX3
from .recadrage_fenetre import centrer_fenetre

longueur = 185
largeur = 165

# Ajouter longueur et largeur pour configuration

class Main:
    def __init__(self) -> None:

        parent = Tk()
        self.parent = parent

        centrer_fenetre(parent, largeur, longueur)

        parent.resizable(True, True)
        parent.title("Parking")

        self.fenetre_connexion = Connexion(parent, self.ouvrir_configuration, self.fermer_configuration, self.fermer_configuration_objets)
        self.fenetre_connexion.place(x=0, y=0)
    
        parent.mainloop()

    def ouvrir_configuration(self, port_actuelle) :

        self.application_configuration = Configuration(self.parent, port_actuelle, self.ouvrir_configuration_objet_SP3, self.ouvrir_configuration_objet_DX3, self.fermer_configuration_objets)
        self.application_configuration.place(x=168, y= 0, width=200, height=300)
    def fermer_configuration(self):

        self.application_configuration.destroy()

    def ouvrir_configuration_objet_SP3(self, dict_des_objets, liste_des_instances_appareil, listbox) :

        self._configuration_objet_SP3 = Configuration_SP3(self.parent, dict_des_objets, liste_des_instances_appareil, listbox)
        self._configuration_objet_SP3.place(x=368, y=0)
    
    def ouvrir_configuration_objet_DX3(self, dict_des_objets, liste_des_instances_appareil, listbox):

        self._configuration_objet_DX3 = Configuration_DX3(self.parent, dict_des_objets, liste_des_instances_appareil, listbox)
        self._configuration_objet_DX3.place(x=368, y=0)

    def fermer_configuration_objets(self) :

        try :
            self._configuration_objet_SP3.destroy()
        except: pass
        try :
            self._configuration_objet_DX3.destroy()
        except: pass