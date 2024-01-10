import serial

def calcul_bcc(adresse_appareil: str, nom_fonction : str, valeur = "") -> str :

    # Vérifie si adresse_appareil est valide avant tout calcul
    try :
        int(adresse_appareil, 16)
    except ValueError :
        raise ValueError("adresse_appareil en hexadecimal!")
    if len(adresse_appareil) != 2 or len(adresse_appareil) != 4 :
         raise ValueError("adresse_appareil doit être de longeur 2 ou 4!") 
         
    
    # Si l'adresse est de 2 octet
    if len(adresse_appareil) == 4 :
        somme = int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(nom_fonction, 16) + int(valeur, 16)
        if somme < 255 :
            bcc = format(somme, "02X")
        elif somme < 65025 :
            bcc = format(somme, "04X")
        else  :
            bcc = format(somme, "06X")
        return bcc

    # Si l'adresse est 1 octet
    elif len(adresse_appareil) == 2 :

        somme = int(adresse_appareil, 16) + int(nom_fonction, 16) + int(valeur, 16)
        if somme < 255 :
            bcc = format(somme, "02X")
        elif somme < 65025 :
            bcc = format(somme, "04X")
        else  :
            bcc = format(somme, "06X")
        return bcc
    else :
        raise ValueError

def envoi_trame(port_serial, adresse_appareil : str, nom_fonction: str, bcc : str, retry : int, valeur = "") -> str :
    
    while retry > 1 :
        # Fabrication de la trame à envoyée
        trame_envoyee = bytes.fromhex(adresse_appareil + nom_fonction + valeur + bcc )

        # Envoie de la trame 
        port_serial.write(trame_envoyee)

        # Reception de la réponse 
        if port_serial.in_waiting > 0:
            trame_reponse = port_serial.read(port_serial.in_waiting)
            if adresse_appareil in trame_reponse :
                return trame_reponse
            else :
                retry -= 1
        else :
            retry -= 1
    raise TimeoutError("L'appareil n'a pas répondu")


class Appareil:
        def __init__(self ,port_serial , modele : str ,version: float, adresse: str) :
            self.port_serial = port_serial
            self.modele = modele
            self.version = version
            self.adresse = adresse

class SP3(Appareil):
        
        def __init__(self, port_serial, version: float, adresse: str):
            super().__init__(port_serial, "SP3", version, adresse)

            # Nombre d'envoie de la trame, avant echec
            self.retry = 5
        
        # Fonction 0x01 | Active ou désactive le mode test du capteur SP3
        def mode_test(self) :
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
        def calibration_potentiomètre(self) :
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
        def potentiomètre(self) :
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


        # Fonction 0x14 | Modifie la valeur du potentimètre digital
        @potentiomètre.setter
        def potentiomètre(self, valeur ) :
            '''
            Modifie la valeur du potentimètre digital

            '''

            # Nom de la fonction
            fonction = "14"

            # Vérifie si la valeur donne est entre 1 et 64
            if valeur < 1 or valeur > 64 :
                raise ValueError("Veuillez saisir une valeur entre 1 et 64")
            
            valeur = str(int(hex(valeur), 16))


            bcc = calcul_bcc(self.adresse, fonction, valeur)
            envoi_trame(self.port_serial, self.adresse, fonction, bcc, self.retry, valeur)

        
             

class DX3(Appareil) :
        def __init__(self, port_serial: str, version: float, adresse: str):
            super().__init__(port_serial, "DX3", version, adresse)