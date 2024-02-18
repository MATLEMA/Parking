from serial import Serial
from .Appareil import Appareil
from .gestion_trame import envoi_trame

class DX3(Appareil):

    def __init__(self,
                 adresse: str,
                 port_serial : Serial,
                 modele : str ,
                 version: float,
                 valeur_fleche: str = "N/A"#TODO supprime
                 ) -> None:
        super().__init__(adresse, port_serial, modele, version)
            
        try :
            valeur_fleche = self.fleche
        except :
            pass

        self.adresse = adresse
        self.port_serial = port_serial
        self.modele = modele
        self.version = version
        self.valeur_fleche = valeur_fleche
    
    # Nombre d'essaie avant echec
    retry = 2

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
    @property
    def fleche(self) -> str:
        """Retourne une valeur hexadecimal

        :raises IndexError: L'appareil n'a pas répondu
        :return: Valeur héxadecimal de la flèche
        :rtype: str

        "01": "droite"
        "02": "haut"
        "03": "gauche"
        "04": "bas"
        "05": "bas-vers-droite"
        "06": "bas-vers-gauche"
        "07": "haut-droit"
        "08": "bas-droit"
        "09": "bas-gauche"
        "0A": "haut-gauche"
        """        
        fleche = {"01": "droite",
                                  "02": "haut",
                                  "03": "gauche",
                                  "04": "bas",
                                  "05": "bas-vers-droite",
                                  "06": "bas-vers-gauche",
                                  "07": "haut-droit",
                                  "08": "bas-droit",
                                  "09": "bas-gauche",
                                  "0A": "haut-gauche"}
        fonction = "4E"
        print("getter fleche")
        reponse = envoi_trame(self.port_serial, self.adresse, fonction, self.retry)[2:4]

        try :
            fleche.get(reponse)
        except:
            raise IndexError("L'appareil n'a pas répondu!")

        return reponse
    
    @fleche.setter
    def fleche(self, valeur : str):

        fonction = "4F"

        if valeur not in ["01","02","03","04","05","06","07","08","09","0A"]:
            raise SyntaxError("Veuillez saisir une valeur compris dans : 01, 02, 03, 04, 05, 06, 07, 08, 09, 0A")
        print("setter fleche")
        envoi_trame(self.port_serial, self.adresse, fonction, self.retry, valeur)