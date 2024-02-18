from tkinter import Tk
from .connexion import Connexion
from .recadrage_fenetre import redefinir_fenetre, centrer_fenetre
from .logique import GestionListbox
from utils import Parking, SP3, DX3

longeur = 185
largeur = 165

class Main:
    def __init__(self) -> None:

        parent = Tk()
        self.parent = parent

        centrer_fenetre(parent, largeur, longeur)

        parent.resizable(False, False)
        parent.title("Parking")

        self.fenetre_connexion = Connexion(parent, self.ouvrir_configuration, self.fermer_configuration, self.fermer_parking)
        self.fenetre_connexion.pack(side="left", anchor= "nw")
    
        parent.mainloop()

    def ouvrir_configuration(self, port_actuelle) :
        
        self.ouvrir_application = GestionListbox(self.parent, port_actuelle)
        self.ouvrir_application.pack(side="left", anchor="nw")

    def fermer_configuration(self):

        self.ouvrir_application.destroy()

    def lancement_parking(self, liste_SP3: list[SP3], liste_DX3: list[DX3]) :

        pass

    def ouvrir_configuration_objet_DX3(self, dict_des_objets, liste_des_instances_appareil, listbox):

        pass

    def fermer_parking(self) :

        pass