from serial import Serial
from .Appareil import Appareil
from .gestion_trame import envoi_trame

class DX3(Appareil):

    def __init__(self,
                 adresse: str,
                 port_serial : Serial,
                 modele : str ,
                 version: float
                 ) -> None:
        super().__init__(adresse, port_serial, modele, version)
        
        valeur_fleche: str = "N/A"
        valeur_parking_plein: str = "N/A"

        try :
            valeur_parking_plein = self.parking_plein
        except :
            pass

        self.adresse = adresse
        self.port_serial = port_serial
        self.modele = modele
        self.version = version
        self.valeur_fleche = valeur_fleche
        self.valeur_parking_plein = valeur_parking_plein
    
    # Nombre d'essaie avant echec
    retry = 1

    def afficheur(self, valeur: str):
        
        try : 
            if int(valeur) < 0 or int(valeur) > 1000 :
                pass
        except :
            ValueError("Veuillez saisir un valeur compris entre 0 et 1.000")
    
        # Formatage 4 deviendra 0004
        valeur = "{:03d}".format(int(valeur))
        fonction = "40"
        hexa_valeur_un = hex(ord(valeur[0]))[2:]
        hexa_valeur_deux = hex(ord(valeur[1]))[2:]
        hexa_valeur_trois = hex(ord(valeur[2]))[2:]

        valeur = (f"0430{hexa_valeur_un}{hexa_valeur_deux}{hexa_valeur_trois}")
        #valeur = "04" + "30" + "34" + "35"
        print("afficheur")
        envoi_trame(self.port_serial, self.adresse, fonction, self.retry, valeur)

    @property
    def parking_plein(self) -> str:

        fonction = "4A"

        reponse: str = envoi_trame(self.port_serial, self.adresse, fonction, self.retry)[2:4]
        return reponse
    
    @parking_plein.setter
    def parking_plein(self, valeur: str) -> None:

        fonction = "4B"

        envoi_trame(self.port_serial, self.adresse, fonction, self.retry, valeur)[2:4]

    @property
    def sens_afficheur(self) -> str:

        fonction = "48"

        reponse: str = envoi_trame(self.port_serial, self.adresse, fonction, self.retry)[2:4]
        return reponse
    
    @sens_afficheur.setter
    def sens_afficheur(self, valeur: str) -> None:

        fonction = "49"

        envoi_trame(self.port_serial, self.adresse, fonction, self.retry, valeur)[2:4]
