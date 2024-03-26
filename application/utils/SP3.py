from serial import Serial
from .appareil import Appareil
from .gestion_trame import envoi_trame
from tkinter import messagebox

class SP3(Appareil):

    retry = 2
    list_SP3 = list()

    def  __init__(self, adresse: str, port_serial: Serial, modele: str):
        super().__init__(adresse, port_serial, modele)
        if adresse not in self.list_SP3:
            self.list_SP3.append(adresse)
        

    # Fonction 0x10 | Retourne si la place est libre ou non 
    @classmethod
    def place_libre(cls, port_serial) -> list[bool] :
        '''
        Retourne si la place est libre ou non
        '''
        # Nom de la fonction 0x10
        fonction = "10"
        liste_reponse: list[bool]= []

        print("thread place libre")
        for i in range(len(cls.list_SP3)):
            reponse: str = envoi_trame(port_serial, cls.list_SP3[i], fonction, cls.retry)

            if reponse[4:6] == "00":
                liste_reponse.append(True)
            else : 
                liste_reponse.append(False)
        return liste_reponse