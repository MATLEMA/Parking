from tkinter import Tk
from .connexion import Connexion
from .recadrage_fenetre import redefinir_fenetre, centrer_fenetre

longeur = 185
largeur = 165

class Main:
    def __init__(self) -> None:

        parent = Tk()
        self.parent = parent

        centrer_fenetre(parent, largeur, longeur)

        parent.resizable(False, False)
        parent.title("Parking")

        self.fenetre_connexion = Connexion(parent, self.ouvrir_configuration, self.fermer_configuration, self.fermer_configuration_objets)
        self.fenetre_connexion.pack(side="left", anchor= "nw")
    
        parent.mainloop()

    def ouvrir_configuration(self, port_actuelle) :
        pass
    def fermer_configuration(self):

        pass

    def ouvrir_configuration_objet_SP3(self, dict_des_objets, liste_des_instances_appareil, listbox) :

        pass
    
    def ouvrir_configuration_objet_DX3(self, dict_des_objets, liste_des_instances_appareil, listbox):

        pass

    def fermer_configuration_objets(self) :

        """ try :
            self._configuration_objet_SP3.destroy()
        except: pass
        try :
            self._configuration_objet_DX3.destroy()
        except: pass """