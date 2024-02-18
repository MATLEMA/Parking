from serial import Serial
from .appareil import Appareil
from .gestion_trame import envoi_trame

class DX3(Appareil):

    retry = 2

    def  __init__(self, adresse: str, port_serial: Serial, modele: str):
        super().__init__(adresse, port_serial, modele)

    def afficheur(self, valeur: str):
        
        try : 
            if int(valeur) < 0 or int(valeur) > 10_000 :
                pass
        except :
            ValueError("Veuillez saisir un valeur compris entre 0 et 10.000")
    
        # Formatage 4 deviendra 0004
        valeur = "{0:04d}".format(int(valeur))
        fonction = "40"
        hexa_valeur_un = hex(ord(valeur[0]))[2:]
        hexa_valeur_deux = hex(ord(valeur[1]))[2:]
        hexa_valeur_trois = hex(ord(valeur[2]))[2:]
        hexa_valeur_quatre = hex(ord(valeur[3]))[2:]

        valeur = f"04{hexa_valeur_un}{hexa_valeur_deux}{hexa_valeur_trois}{hexa_valeur_quatre}"
        #valeur = "04" + "30" + "34" + "35" + "37"
        print("afficheur")
        envoi_trame(self.port_serial, self.adresse, fonction, self.retry, valeur)

        ######### IL SE PEUT QUE LE DX3 NE PEUT QUE PRENDRE 3 CARACTERES NON 4###################