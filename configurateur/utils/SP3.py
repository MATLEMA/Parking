from serial import Serial
from .gestion_trame import envoi_trame
from .Appareil import Appareil

class SP3(Appareil):

    def __init__(
            self,
            adresse: str,
            port_serial : Serial,
            modele : str ,
            version: float,
            ) -> None:
        super().__init__(adresse, port_serial, modele, version)
            
        try :
            valeur_potentiometre = self.potentiometre
            valeur_distance_maximal = self.distance_maximal
            mode_detection = self.mode_detection
            mode_transceiver = self.transceiver
            _place_libre = self.place_libre()
        except :
            self.valeur_potentiometre = "N/A"
            self.valeur_distance_maximal = "N/A"
            self._mode_detection = "N/A"
            self.mode_transceiver = "N/A"
            self._place_libre = "N/A"

        self.adresse = adresse
        self.port_serial = port_serial
        self.modele = modele
        self.version = version

    # Nombre d'envoie de la trame, avant echec
    retry = 1
        
    # Fonction 0x01 | Active ou désactive le mode test du capteur SP3
    def mode_test(self)  -> None:
        '''
        Active ou désactive le mode test du capteur SP3\n
        Mode normal -> Mode test
        Mode test -> Mode normal\n
        Cette fonction permet de savoir si le capteur SP3 détecte le sol\n
        En mode test le capteur clignotera\n
        Test réussi = clignotement de quelques secondes\n
        Test non réussi = clignotement infinie 
        '''
        # Nom de la fonction 
        fonction = "01"
        print("mode test")
        envoi_trame(self.port_serial, self.adresse, fonction, self.retry)
                
        # Fonction 0x02 | Active ou désactive la calibration du potentiomètre
    def calibration_potentiomètre(self)  -> None:
        '''
        Active ou désactive la calibration du potentiomètre\n
        Mode normal -> Mode calibration
        Mode calibration -> Mode normal\n
        Si la calibration est déja active, cela l'annulera.
        '''
        # Nom de la fonction
        fonction = "02"

        print("calibration auto")
        envoi_trame(self.port_serial, self.adresse, fonction, self.retry)

    # Fonction 0x04 | Retourne la valeur du potentiomètre digital
    @property
    def potentiometre(self) -> str :
        '''
        Retourne la valeur du potentiomètre digital
            
        '''
        # Nom de la fonction 
        fonction = "04"

        print("getter potentiomètre")
        reponse = str(int(envoi_trame(self.port_serial, self.adresse, fonction, self.retry)[4:6], 16))

        # La valeur du potentiomètre digital se trouve sur le 3ème octet de la trame réponse
        self.valeur_potentiometre = reponse
        return reponse

    # Fonction 0x14 | Modifie la valeur du potentiomètre digital
    @potentiometre.setter
    def potentiometre(self, valeur : str ) -> bool :
        '''
        Modifie la valeur du potentiomètre digital\n
        La fonction confirme que l'appareil à répondu
        '''

        # Nom de la fonction
        fonction = "14"

        # Vérifie si la valeur donne est entre 1 et 64
        try :
            if int(valeur) <= 1 or int(valeur) >= 64 :
                pass
        except:
            raise ValueError("Veuillez saisir une valeur entre 1 et 64")
        
        valeur = hex(int(valeur))[-2:]

        print("setter potentiometre")
        reponse: str = envoi_trame(self.port_serial, self.adresse, fonction, self.retry, valeur)

        if reponse == self.adresse :
            return True
        else :
            return False

    # Fonction 0x06 | Retourne la distance de détection maximal du capteur 
    @property
    def distance_maximal(self) -> int :
        '''
        Retourne la distance de détection maximal du capteur :
        '''
        # Nom de la fonction 
        fonction = "06"

        print("getter distance maximal")
        reponse = envoi_trame(self.port_serial, self.adresse, fonction, self.retry)
        print(reponse)

        # La valeur de la distance maximal se trouve sur le 3ème octet de la trame réponse
        limite_superieur = 80 + int(reponse[4:6], 16) * 10 - 1
        print(limite_superieur)

        if limite_superieur < 400 and reponse[4:6] != "15" and reponse[4:6] != "16" :
            self.valeur_distance_maximal = limite_superieur
            return limite_superieur

        elif reponse[4:6] == "15" :
            self.valeur_distance_maximal = 380
            return 380
        else : 
            self.valeur_distance_maximal = 400
            return 400
            
    # Fonction 0x11 | Modifie la distance maximal du capteur
    @distance_maximal.setter
    def distance_maximal(self, valeur : str) -> bool :
        '''
        Modifie la distance maximal du capteur
        Intervalle = [150,?[\n
        La fonction confirme que l'appareil à répondu
        '''
        # Nom de la fonction 
        fonction = "11"

        try:
            if int(valeur) < 150 :
                raise
        except:
            raise ValueError("Veuillez saisir une valeur entre 150 et (259)")    
            
        valeur = hex(int(valeur)//10 * 10)[2:]

        print("setter distance maximal")
        reponse = envoi_trame(self.port_serial, self.adresse, fonction, self.retry, valeur)

        if reponse[4:6] == "00" :
            return True
        else :
            return False

    # Fonction 0x07 | Retourne le mode de détection du capteur
    @property
    def mode_detection(self) -> bool :
        '''
        Retourne le mode de détection du capteur 
        getter | True = prise en compte de la détection du sol
        '''
        # Nom de la fonction 
        fonction = "07"

        print("getter mode détection")
        reponse = envoi_trame(self.port_serial, self.adresse, fonction, self.retry)

        if reponse[4:6] == "00" :
            self._mode_detection = True
            return True
        else :
            self._mode_detection = False
            return False
    
    # Fonction 0x12 | Modifie le mode de détection du capteur
    @mode_detection.setter
    def mode_detection(self, valeur : bool) -> bool :
        '''
        Modifie le mode de détection du capteur 
        getter | True = prise en compte de la détection du sol
        setter | True = l'appareil à bien recu la trame
        '''
        # Nom de la fonction 
        fonction = "12"

        if valeur == True : 
            mode_detection : str = "00"
        else : 
            mode_detection : str = "FF"

        print("setter mode détection")
        reponse = envoi_trame(self.port_serial, self.adresse, fonction, self.retry, mode_detection)

        if reponse[4:6] == "00" :
            return True
        else :
            return False

    # Fonction 0x03 | Retourne le mode de reception/transmission ultrason
    @property
    def transceiver(self) -> bool :
        '''
        Retourne le mode de reception/transmission ultrason 
        getter | Si l'appareil est en mode réception : False
        Si l'apprareil est en mode réception/transmission : True\n
        ''' 
        # Nom de la fonction 
        fonction = "03"

        print("getter transceiver")
        reponse = envoi_trame(self.port_serial, self.adresse, fonction, self.retry)
        
        if reponse[4:6] == "00" :
            self.mode_transceiver = False
            return False
        else :
            self.mode_transceiver = True
            return True
        
    # Fonction 0x13 | Modifie le mode de reception/transmission ultrason
    @transceiver.setter
    def transceiver(self, valeur : bool) -> None :
        '''
        Modifie le mode de reception/transmission ultrason
        La fonction confirme que l'appareil à répondu
        '''
        # Nom de la fonction
        fonction = "13"

        if valeur == False : 
            # En mode reception
            mode_reception_transmission : str = "00"
        else : 
            # En mode reception/transmission
            mode_reception_transmission : str = "FF"

        print("setter transceiver")
        reponse = envoi_trame(self.port_serial, self.adresse, fonction, self.retry, mode_reception_transmission)

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
            self._place_libre = True
            return True
        else : 
            self._place_libre = False
            return False

    # Fonction 0x19 | 0x1A | 0x1B | Force les leds à devenir verte, rouge, orange
    def couleur(self, couleur: str)  -> None:
        
        dict_couleur_fonction: dict[str, str] = {"vert" : "19", "rouge" : "1A", "orange": "1B"}

        if couleur.lower() not in dict_couleur_fonction.keys() :
            raise SyntaxError("Les couleurs valide sont vert, rouge et orange")
        
        # Connaitre le nom de la fonction voulu
        fonction = dict_couleur_fonction[couleur]
        print("couleur SP3")
        envoi_trame(self.port_serial, self.adresse, fonction, self.retry)
        
    # Fonction 0x15 | Force le capteur à clignoter lorsque la place est libre
    def clignoter_libre(self)  -> None:
        '''
        Force le capteur à clignoter lorsque la place est libre
        Pour l'instant temps = 100 = 10s
        '''

        # Nom de la fonction 
        fonction = "15"
        print("clignoter SP3")
        envoi_trame(self.port_serial, self.adresse, fonction, self.retry, valeur="64")