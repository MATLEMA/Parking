from serial import Serial
from .appareil import Appareil
from .gestion_trame import envoi_trame
from tkinter import messagebox

class SP3(Appareil):

    retry = 2
    def  __init__(self, adresse: str, port_serial: Serial, modele: str):
        super().__init__(adresse, port_serial, modele)

    # Fonction 0x10 | Retourne si la place est libre ou non 
    def place_libre(self) -> bool :
        '''
        Retourne si la place est libre ou non
        '''
        # Nom de la fonction 0x10
        fonction = "10"

        print("thread place libre")
        reponse = envoi_trame(self.port_serial, self.adresse, fonction, self.retry)

        if reponse[4:6] == "00":
            self.__place_libre = True
            return True
        else : 
            self.__place_libre = False
            return False