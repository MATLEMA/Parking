from serial import Serial
import threading

def calcul_bcc(adresse_appareil: str, nom_fonction : str, valeur = "")   -> str :

    # Vérifie si adresse_appareil est valide avant tout calcul
    try :
        int(adresse_appareil, 16)
    except ValueError :
        raise ValueError("adresse_appareil en hexadecimal!")

    if len(adresse_appareil) not in [2, 4] :
         raise ValueError("adresse_appareil doit être de longeur 2 ou 4!") 
         
    
    # Si l'adresse est de 2 octet
    if len(adresse_appareil) == 4 :
        if valeur == "" :
            somme = int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(nom_fonction, 16) 
        else : 
            somme = int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(nom_fonction, 16) + int(valeur, 16)

        bcc = format(int(str(somme)[0:2]), "02X")

        return bcc

    # Si l'adresse est 1 octet
    elif len(adresse_appareil) == 2 :

        if valeur == "" :
            somme = int(adresse_appareil, 16) + int(nom_fonction, 16)
        else : 
            somme = int(adresse_appareil, 16) + int(nom_fonction, 16) + int(valeur, 16)

        bcc = format(int(str(somme)[0:2]), "02X")

        return bcc
    else :
        raise ValueError

def envoi_trame(port_serial: Serial, adresse_appareil : str, nom_fonction: str, bcc : str, retry : int, valeur = "") -> str :
    
    while retry > 0 :
        # Fabrication de la trame à envoyée
        trame_envoyee: bytes = bytes.fromhex(adresse_appareil + nom_fonction + valeur + bcc )

        # Envoie de la trame 
        port_serial.write(trame_envoyee)

        # Reception de la réponse 
        if port_serial.in_waiting > 0:
            trame_reponse = port_serial.read(port_serial.in_waiting)
            trame_reponse = trame_reponse.hex()
            if adresse_appareil in trame_reponse :
                return trame_reponse
            else :
                retry -= 1
        else :
            retry -= 1
    raise TimeoutError("L'appareil n'a pas répondu")

class Appareil:
    def __init__(self , adresse: str, port_serial : Serial, modele : str ,version: float) :
        self.port_serial = port_serial
        self.modele = modele
        self.version = version
        self.adresse = adresse

class SP3(Appareil):

        def __init__(
                self ,
                adresse: str,
                port_serial : Serial,
                modele : str ,
                version: float,
                valeur_potentiometre :str = "N/A",
                valeur_distance_maximal: int | str = "N/A",
                mode_detection: bool | str = "N/A",
                mode_transceiver: bool | str = "N/A",
                _place_libre: bool | str = "N/A"
                ):
            super().__init__(adresse, port_serial, modele, version)
            

            try :
                valeur_potentiometre = self.potentiometre
                valeur_distance_maximal = self.distance_maximal
                mode_detection = self.mode_detection
                mode_transceiver = self.transceiver
                _place_libre = self.place_libre()
            except :
                pass

            self.adresse = adresse
            self.port_serial = port_serial
            self.modele = modele
            self.version = version
            self.valeur_potentiometre = valeur_potentiometre
            self.valeur_distance_maximal = valeur_distance_maximal
            self._mode_detection = mode_detection
            self.mode_transceiver = mode_transceiver
            self._place_libre = _place_libre

        # Nombre d'envoie de la trame, avant echec
        retry = 5
        
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

                bcc = calcul_bcc(self.adresse, fonction)
                envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry)
                
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

            bcc = calcul_bcc(self.adresse, fonction)
            envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry)

        # Fonction 0x04 | Retourne la valeur du potentiomètre digital
        @property
        def potentiometre(self) -> str :
            '''
            Retourne la valeur du potentiomètre digital
             
            '''

            # Nom de la fonction 
            fonction = "04"

            bcc = calcul_bcc(self.adresse, fonction)
            reponse = envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry)

            # La valeur du potentiomètre digital se trouve sur le 3ème octet de la trame réponse
            valeur_potentiometre = reponse[4:6]
            return valeur_potentiometre

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
            if int(valeur) < 1 or int(valeur) > 64 :
                raise ValueError("Veuillez saisir une valeur entre 1 et 64")
            
            valeur = str(int(hex(int(valeur)), 16))


            bcc = calcul_bcc(self.adresse, fonction, valeur)
            reponse = envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry, valeur)
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

            bcc = calcul_bcc(self.adresse, fonction)
            reponse = envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry)

            # La valeur de la distance maximal se trouve sur le 3ème octet de la trame réponse
            i = int(reponse[4:6], 16)
            limite_superieur = 80 + i * 10 - 1
            if limite_superieur < 400 and reponse[4:6] != "15" and reponse[4:6] != "16" :
                return limite_superieur

            elif reponse[4:6] == "15" :
                return 380
            else : 
                return 400
             
        # Fonction 0x11 | Modifie la distance maximal du capteur
        @distance_maximal.setter
        def distance_maximal(self, valeur ) -> bool :
            '''
            Modifie la distance maximal du capteur
            Intervalle = [150,?[\n
            La fonction confirme que l'appareil à répondu
            '''
            # Nom de la fonction 
            fonction = "11"

            if int(valeur) < 150 :
                raise ValueError("Veuillez saisir une valeur entre 1 et 64")
            
            valeur = valeur//10 * 10
            valeur = hex(valeur)[2:]

            bcc = calcul_bcc(self.adresse, fonction, valeur)
            reponse = envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry, valeur)
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

            bcc = calcul_bcc(self.adresse, fonction)
            reponse = envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry)

            if reponse[4:6] == "00" :
                return True
            else :
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

            bcc = calcul_bcc(self.adresse, fonction)
            reponse = envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry, mode_detection)

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

            bcc = calcul_bcc(self.adresse, fonction)
            reponse = envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry)
            
            if reponse[4:6] == "00" :
                return False
            else :
                return True
            
        # Fonction 0x13 | Modifie le mode de reception/transmission ultrason
        @transceiver.setter
        def transceiver(self, valeur : bool) -> bool :
            '''
            Modifie le mode de reception/transmission ultrason
            La fonction confirme que l'appareil à répondu
            '''
            # Nom de la fonction
            fonction = "13"
            if valeur == True : 
                # En mode reception
                mode_reception_transmission : str = "00"
            else : 
                # En mode reception/transmission
                mode_reception_transmission : str = "FF"

            bcc = calcul_bcc(self.adresse, fonction)
            reponse = envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry, mode_reception_transmission)

            if reponse == self.adresse :
                return True
            else : 
                return False
            
        # Fonction 0x10 | Retourne si la place est libre ou non 
        def place_libre(self) -> bool :
            '''
            Retourne si la place est libre ou non
            '''
            # Nom de la fonction 0x10
            fonction = "10"

            bcc = calcul_bcc(self.adresse, fonction)
            reponse = envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry)

            if reponse[4:6] == "00":
                return True
            else : 
                return False

        # Fonction 0x19 | 0x1A | 0x1B | Force les leds à devenir verte, rouge, orange
        def couleur(self, couleur: str)  -> None:
            
            dict_couleur_fonction: dict[str, str] = {"vert" : "19", "rouge" : "1A", "orange": "1B"}

            couleur = couleur.lower()
            if couleur not in dict_couleur_fonction.keys() :
                raise SyntaxError("Les couleurs valide sont vert, rouge et orange")
            
            # Connaitre le nom de la fonction voulu
            fonction = dict_couleur_fonction[couleur]

            bcc = calcul_bcc(self.adresse, fonction)
            envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry)
            
        # Fonction 0x15 | Force le capteur à clignoter lorsque la place est libre
        def glignoter_libre(self)  -> None:
            '''
            Force le capteur à clignoter lorsque la place est libre
            Pour l'instant temps = 100 = 10s
            '''

            # Nom de la fonction 
            fonction = "15"

            bcc = calcul_bcc(self.adresse, fonction)
            envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry, valeur="64")

class DX3(Appareil) :
        
        def hello(self):
            pass