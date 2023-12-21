import serial

class Appareil:
        def __init__(self ,port_serial , modele : str ,version: float, adresse: str) :
            self.port_serial = port_serial
            self.modele = modele
            self.version = version
            self.adresse = adresse

        # Active ou désactive le mode test du capteur    
        def fonction0x01(self) :  
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
            Elle sert à activer ou désactiver le mode test du capteur
            A la réception de la trame, si l'appareil est en mode test, il clignotera, si il cesse au bout de quelques secondes il détecte le sol, sinon il ne le détecte pas  
            La trame envoye 4 octets
            La trame reçu est de 2 octets 
            '''
            fonction = "01"
            bcc = hex(int(self.adresse[0:2], 16) + int(self.adresse[2:4], 16)+ int(fonction, 16))[2:]
            trame = bytes.fromhex(self.adresse + fonction + bcc)
            self.port_serial.write(trame)
            reponse_appareil = self.port_serial.read(2).hex()
            if reponse_appareil == "" :
                raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")

        # Active / désactive la calibration du potentiomètre 
        def fonction0x02(self) :
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
            Elle sert à activer ou désactiver la calibration du potentiomètre
            A la réception de la trame, si l'appareil est en état normal, il passera en mode processus d'étalonnage automatique, sinon il arretera immédiatement le mode d'étalonnage et n'enregistra aucun données en mémoire
            La trame envoye 4 octets
            La trame reçu est de 2 octets 
            '''
            fonction = "02"
            bcc = hex(int(self.adresse[0:2], 16) + int(self.adresse[2:4], 16)+ int(fonction, 16))[2:] 
            trame = bytes.fromhex(str(self.adresse + fonction + bcc))
            self.port_serial.write(trame)
            reponse_appareil = self.port_serial.read(2).hex()
            if reponse_appareil == "" :
                raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")

        # Retourne si l'appareil est en mode reception ou reception/transmission
        def fonction0x03(self) :
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
            Elle sert à retourner si l'appareil est en mode réception ou réception/transmission
            La trame envoye 4 octets
            La trame reçu est de 4 octets
            La fonction retourne une valeur 
            Si l'appareil est en mode réception : False
            Si l'apprareil est en mode réception/transmission : True
            '''
            fonction = "03"
            bcc = hex(int(self.adresse[0:2], 16) + int(self.adresse[2:4], 16)+ int(fonction, 16))[2:]
            trame = bytes.fromhex(str(self.adresse + fonction + bcc))
            self.port_serial.write(trame)
            reponse_appareil = self.port_serial.read(4).hex()
            if reponse_appareil == "" :
                raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")
            if reponse_appareil[4:6] == "00" :
                print("L'appareil est en mode réception")
                is_transmission = False
            else :
                print("L'appareil est en mode transmission/réception")
                is_transmission = True
            return is_transmission

        # Retourne la valeur du potentiomètre digital (1 à 64)        
        def fonction0x04(self) :
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
            Elle sert à retourner la valeur du potentiomètre digital
            La trame envoye 4 octets
            La trame reçu est de 4 octets
            La fonction retourne une valeur entre 1 à 64 (décimal ou hexa?)
            Réglage de la fréquence de rafraichissement ? ou bien de la sensibilité du capteur
            '''
            fonction = "04"
            bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16)+ int(fonction, 16))[2:]
            trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
            port_serial.write(trame)
            reponse_appareil = port_serial.read(4).hex()
            if reponse_appareil == "" :
                raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")
            valeur = int(reponse_appareil[4:6], 16)
            return valeur

        # Recherche les informations d'un équipement (Nom de l'équipement | version)
        def fonction0x05(port_serial, adresse_appareil) :
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
            Elle sert à retourner le nom de l'équipement ainsi 
            La trame envoye 4 octets
            La trame reçu est de 4 octets
            La fonction retourne une valeur entre 1 à 64 (décimal ou hexa?)
            Réglage de la fréquence de rafraichissement ? ou bien de la sensibilité du capteur
            '''
            fonction = "05"
            nom_appareil = None

            dictionnaire_nom_hexa: dict[str,str] = {"SP1": "02", "D3": "02", "MR4/dp": "0x23", "D4": "0x2E", "DX2-VMS": "0x3B", "DX4-VMS": "0x3D", "DXCA": "0x44", "SP2": "0x1D", "DX3": "0x1E", "DX2": "0x2D", "SP3": "0x2B", "DX3-VMS": "0x3C", "DX-VMS-F": "0x3E", "GS24x8RGB": "0x3F"}
            if len(adresse_appareil) == 4 :
                bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16))[2:]
                trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
                reponse_appareil = port_serial.read(5).hex()
                if reponse_appareil == "" :
                    raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")   
                modele_appareil_hexa = reponse_appareil[4:6]   
                for cle, valeur in dictionnaire_nom_hexa.items() :
                    if modele_appareil_hexa == valeur:
                        nom_appareil = cle
                        break

                # Détection de la version de l'objet
                version_appareil = reponse_appareil[6:8]
                version_appareil = int(version_appareil, 16)/10                                            # 0x1A = 10 (decimal) = version 1.0
                return nom_appareil, version_appareil, True
                    
            elif len(adresse_appareil) == 2 :
                bcc = hex(int(adresse_appareil, 16) + int(fonction, 16))[2:]
                trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
                port_serial.write(trame)
                reponse_appareil = port_serial.read(4).hex()
                modele_appareil_hexa = reponse_appareil[2:4]
                for cle, valeur in dictionnaire_nom_hexa.items() :
                    if modele_appareil_hexa == valeur:
                        nom_appareil = cle
                        break

                # Détection de la version de l'objet
                version_appareil = reponse_appareil[6:8]
                version_appareil = int(version_appareil, 16)/10
                return nom_appareil, version_appareil, True

            else : 
                sys.exit("Il y a eu une erreur !")

        # Retourne la distance de détection maximal du capteur
        def fonction0x06(port_serial, adresse_appareil) :
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
            Elle sert à Retourner la distance de détection maximal du capteur
            La trame envoye 4 octets
            La trame reçu est de 4 octets
            La fonction retourne une valeur entre entre 150 et 400
            '''
            fonction = "06"
            bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16))[2:]
            trame = bytes.fromhex(adresse_appareil + fonction + bcc)
            port_serial.write(trame)
            reponse_port = port_serial.read(4).hex()

            i = int(reponse_port[4:6], 16)
            limite_inferieur = 70 + i * 10
            limite_superieur = 80 + i * 10 - 1
            if limite_superieur < 400 and reponse_port[4:6] != "15" and reponse_port[4:6] != "16" :
                print(f"La distance de détection est entre {limite_inferieur} et {limite_superieur} cm")
                return limite_superieur

            elif reponse_port[4:6] == "15" :
                print(f"La distance de détection est entre 380 et 399 cm")
                return 380
            else : 
                print(f"La distance de détection est au dessus de 400 cm")
                return 400

        # Retourne le mode de détection du capteur
        def fonction0x07(port_serial, adresse_appareil) :
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
            Elle sert à retourner le mode de détection du capteur
            La trame envoye 4 octets
            La trame reçu est de 4 octets
            La fonction retourne si oui ou non le capteur prend en compte la détectoin du sol  ?
            '''
            fonction = "07"
            bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16))[2:]
            trame = bytes.fromhex(adresse_appareil + fonction + bcc)
            port_serial.write(trame)
            reponse_port = port_serial.read(4).hex()
            if reponse_port[4:6] == "00" :
                print("L'appareil prendra en compte la détection du sol pour décider de son état")
                return True
            else :
                print("L'appareil ne prendra pas en compte la détection du sol pour décider de son état")
                return False

        # Retourne le mode d'étalonnage du capteur 
        def fonction0x09(port_serial, adresse_appareil) :
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
            Elle sert à retourner le mode d'étalonnage du capteur
            La trame envoye 4 octets
            La trame reçu est de 4 octets
            La fonction ne retourne en elle-même ne retourne rien
            '''
            fonction = "09"
            bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16))[2:]
            trame = bytes.fromhex(adresse_appareil + fonction + bcc)
            port_serial.write(trame)
            reponse_port = port_serial.read(4).hex()
            reponse_type_binaire= bin(int(reponse_port[4:6],16))[7:]

            if reponse_type_binaire[0] == 1 :
                print("L'appareil est en mode d'étalonnage au sol autonome.")
            else : 
                print("L'appareil n'est pas en mode d'étalonnage au sol autonome")

            if reponse_type_binaire[1] == 1 :
                print("L'appareil est en train de s'étalonner")
            else : 
                print("L'appareil n'est pas en train de s'étalonner")

            if reponse_type_binaire[2] == 1 :
                print("L'appareil est en mode d'étalonnage au sol")
            else : 
                print("L'appareil n'est pas en mode d'étalonnage au sol")    

        # Renvoie si la place est libre ou non 
        def fonction0x10(port_serial, adresse_appareil) :
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
            Elle sert à retourner si la place est libre ou non 
            La trame envoye 4 octets
            La trame reçu est de 4 octets
            La fonction retourne un type booléen
            '''
            fonction = "10"
            bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16))[2:] 
            trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
            port_serial.write(trame)
            reponse_port = port_serial.read(4).hex()
            if reponse_port == "" :
                raise NameError(f"Le capteur {adresse_appareil} n'est pas connecter ! ou n'a pas répondu !")
            if reponse_port[4:6] == "00":
                is_open = True
            else : 
                is_open = False
            return is_open

        # Modifie la distance maximal de detection
        def fonction0x11(port_serial, adresse_appareil, distance) :
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial, l'adresse_appareil ainsi qu'une distance (en cm) entre 150 et l'infinie?
            Elle sert à modifier la distance maximal de détection
            La trame envoye 5 octets
            La trame reçu est de 4 octets
            La fonction retourne un type booléen
            True : La fonction à bien modifié la distance maximal\n
            Exemple :
            >>> x = fonction0x11(4F51, 165)
            True
            '''
            fonction = "11"
            if distance < 150 :
                raise NameError("Veuillez saisir un nombre superieur à 150cm")
            distance = distance//10 * 10
            distance = hex(distance)[2:]
            bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16) + int(distance, 16))[2:]
            trame = bytes.fromhex(adresse_appareil + fonction + distance + bcc)
            port_serial.write(trame)
            reponse_port = port_serial.read(4).hex()
            if reponse_port[4:6] == "00" :
                return True
            else :
                return False

        # Modifie le mode de détection 
        def fonction0x12(port_serial, adresse_appareil, mode : bool) :
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial, de l'adresse de l'appareil ainsi que le mode voulu (bool)
            Elle sert à modifier le mode de détection du capteur
            La trame envoye 5 octets
            La trame reçu est de 4 octets
            La fonction retourne un type booléen
            Exemple :
            >>> x = fonction0x12(4F51, False)
            True
            '''
            fonction = "12"
            if mode == True : 
                mode_detection : str = "00"
            else : 
                mode_detection : str = "FF"
            bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16) + int(mode_detection, 16))[2:]
            trame = bytes.fromhex(adresse_appareil + fonction + mode_detection + bcc)
            port_serial.write(trame)
            reponse_port = port_serial.read(4).hex()
            if reponse_port[4:6] == "00" :
                return True
            else :
                return False

        # Modifie le capteur en mode reception ou reception/transmission
        def fonction0x13(port_serial, adresse_appareil, mode : bool) :
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial, de l'adresse de l'appareil ainsi que le mode voulu (bool)
            Elle sert à modifie le capteur en mode reception ou reception/transmission
            La trame envoye 5 octets
            La trame reçu est de 2 octets
            '''
            fonction = "13"
            if mode == True : 
                # En mode reception
                mode_reception_transmission : str = "00"
            else : 
                # En mode recpetion/transmission
                mode_reception_transmission : str = "FF"
            bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16) + int(mode_reception_transmission, 16))[2:]
            trame = bytes.fromhex(adresse_appareil + fonction + mode_reception_transmission + bcc)
            port_serial.write(trame)
            reponse_port = port_serial.read(4).hex()       # Voir si cela ne casse pas qq chose quand enlevé

        # Modifie la valeur du potenctiomètre digital
        def fonction0x14(port_serial, adresse_appareil, valeur) :
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial, de l'adresse de l'appareil ainsi qu'une valeur comprise entre 1 et 64
            Elle sert à modifie la valeur du potentiomètre digital
            La trame envoye 5 octets
            La trame reçu est de 2 octets
            '''
            if valeur < 1 or valeur > 64 :
                raise NameError("Veuillez saisir une valeur entre 1 et 64")
            fonction = "14"
            valeur = hex(int(valeur))
            bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16) + int(valeur, 16))[2:]
            trame = bytes.fromhex(adresse_appareil + fonction + valeur + bcc)
            port_serial.write(trame)
            reponse_port = port_serial.read(4).hex()       # Voir si cela ne casse pas qq chose quand enlevé

        # Force le capteur à clignoter lorsque le siège est libre
        def fonction0x15(port_serial, adresse_appareil, temps) :
            '''
            Cette fonction à besoin d'un port ouvert donné par la variable port_serial, de l'adresse de l'appareil ainsi qu'une valeur de temps(en ms) mutliple de 100ms et ne doit pas dépasser 
            Elle sert à modifie la valeur du potentiomètre digital
            La trame envoye 5 octets
            La trame reçu est de 2 octets
            '''
            if temps >= 256 or temps <= 0 :
                raise NameError("Veuillez saisir une valeur de temps entre 1 et 255")
            fonction = "15"
            temps = hex(int(temps))
            bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16) + int(temps, 16))[2:]
            trame = bytes.fromhex(adresse_appareil + fonction + temps + bcc)
            port_serial.write(trame)
            reponse_port = port_serial.read(4).hex()       # Voir si cela ne casse pas qq chose quand enlevé

        # Force les leds à devenir de couleur verte
        def fonction0x19(port_serial, adresse_appareil) :
            fonction = "19"
            bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16))[2:] 
            trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
            port_serial.write(trame)
            reponse_port = port_serial.read(4).hex()       # Voir si cela ne casse pas qq chose quand enlevé

        # Force les leds à devenir de couleur rouge
        def fonction0x1A(port_serial, adresse_appareil) :
            fonction = "1A"
            bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16))[2:] 
            trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
            port_serial.write(trame)
            reponse_port = port_serial.read(4).hex()       # Voir si cela ne casse pas qq chose quand enlevé

        # Force les leds à devenir de couleur orange
        def fonction0x1B(port_serial, adresse_appareil) :
            fonction = "1B"
            bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16))[2:] 
            trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
            port_serial.write(trame)
            reponse_port = port_serial.read(4).hex()       # Voir si cela ne casse pas qq chose quand enlevé
    
