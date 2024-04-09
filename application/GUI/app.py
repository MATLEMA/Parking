from tkinter import Tk
from .connexion import Connexion
from .recadrage_fenetre import redefinir_fenetre, centrer_fenetre
from .logiqueDX3 import GestionListboxDX3
from .logiqueSP3 import GestionListboxSP3
from .calculateur import Launch
from utils import Parking, SP3, DX3
from serial import Serial

longeur = 185
largeur = 165

class Main:
    def __init__(self) -> None:

        parent = Tk()
        self.parent: Tk = parent

        centrer_fenetre(parent, largeur, longeur)

        parent.resizable(True, True)
        parent.title("Parking")

        self.fenetre_connexion = Connexion(parent, ouvrir_gestion_DX3=self.ouvrir_gestion_DX3, fermer_gestion_DX3=self.fermer_gestion_DX3, ouvrir_parking=self.ouvrir_parking, fermer_gestion_SP3=self.fermer_gestion_SP3, fermer_parking=self.fermer_parking, )
        self.fenetre_connexion.place(x= 0, y= 0)
    
        parent.mainloop()

    def ouvrir_gestion_DX3(self, port_actuelle: Serial) :
        self.port_actuelle: Serial = port_actuelle
        
        self.gestion_DX3 = GestionListboxDX3(self.parent, port_actuelle, self.ouvrir_gestion_SP3)
        self.gestion_DX3.place(x=168, y= 0)

    def fermer_gestion_DX3(self):

        self.gestion_DX3.destroy()

    def ouvrir_gestion_SP3(self, liste_DX3: DX3):

        self.adresse_DX3 = liste_DX3
        self.gestion_SP3 = GestionListboxSP3(self.parent, self.port_actuelle, self.ouvrir_parking)
        self.gestion_SP3.place(x=368, y= 0)
    
    def fermer_gestion_SP3(self):

        self.gestion_SP3.destroy()

    def ouvrir_parking(self) :
        
        self.launch = Launch(self.parent, self.port_actuelle, self.adresse_DX3)
        self.launch.place(x=235, y= 270)


    def fermer_parking(self) :

        self.launch.destroy()