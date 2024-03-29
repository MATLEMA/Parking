import serial
import serial.tools.list_ports
import threading
try :
    from .SP3 import Appareil
    from utils.SP3 import Appareil
except:
    pass
from time import sleep


# Variables : 
port : str                              # Dossier du port COM sélectionné
baudrate : int                          # Baudrate
timeout : float                         # Timeout port

############################################################################################################################################################################

# Teste si le port est ouvert 
def connecter(port, baudrate, timeout):
    baudrate = int(baudrate)
    timeout = float(timeout)

    try :
        serial.Serial(port, baudrate, timeout= timeout)
        return True
    except serial.SerialException :
        return False

############################################################################################################################################################################
    
# Listing des ports // Doit marcher sur linux et windows !! 
if __name__ == "__main__" :
    listing_des_ports = serial.tools.list_ports.comports()                                                                                                   # Création d'une liste sous forme de class ListPortInfo
    print(f"Nom   Description\n")          

    # Boucle qui passe par tout les paramètres de la class ListPortInfo de notre variable listing_des_ports
    for information_port_disponible in listing_des_ports :
        print(f"{information_port_disponible.device} | {information_port_disponible.description} | {information_port_disponible.interface}\n")

# Liste les port sur la machine
def listing_port() :
    dictionnaire_port : list[str] = []
    listing_des_ports = serial.tools.list_ports.comports()                                                                                                   # Création d'une liste sous forme de class ListPortInfo

    # Boucle qui passe par tout les paramètres de la class ListPortInfo de notre variable listing_des_ports
    for information_port_disponible in listing_des_ports :
        dictionnaire_port.append(information_port_disponible.device)
    return dictionnaire_port

# Ceci est un test pour voir si le port donné par l'utilisateur est ouvert
def test_port_ouvert() :
    '''
    Ceci est un test pour voir si le port donné par l'utilisateur est ouvert
    L'utilisateur va grâce au listing des ports sélectionner son port 
    Puis son baud rate /! Certains appareils ne peuvent pas supporter des valeurs de 9600 ou 19200 !
    Puis le timeout
    Si la vérification à échouer au test recommencera et l'utilisateur rentrera à nouveau les paramètres 
    Les paramètres suites à ce test seront conserver dans des variables et ne pourront en aucun cas être changé.
    '''
    while True :
        # Boucle pour l'adressage du port 
        while True :
            try : 
                port = str(input("Veuillez saisir l'adresse du port : "))
                break
            except ValueError : 
                print("*Erreur type : Valeur ")

        # Boucle pour l'adressage du baudrate
        while True :
            list_baudrate_possible = [19200,9600,4800] 
            baudrate = int(input(f"Veuillez saisir le nombre de bit/s ({list_baudrate_possible}): "))
            if baudrate in list_baudrate_possible :
                break
            else : 
                print(f"Veuillez choisir entre {list_baudrate_possible}")
        # Boucle pour l'adressage du timeout
        while True :
            try :
                timeout = float(input("Veuillez saisir un timeout : "))
                break
            except ValueError :
                print("Veuillez saisir un reel")

        # Vérification si le port est ouvert 
        # Si oui les variables seront stockées
        try :
            port_serial = serial.Serial(port, baudrate=baudrate, write_timeout=0, timeout=timeout)
            break
        except serial.SerialException :
            print(f"Le port {port} n'est pas ouvert réessayer avec un autre port ou verifier votre installation !")
    return port, baudrate, timeout, port_serial

# Détection automatique de tous les appareils connectés en réseau serie
def detection_appareil(port_serial, stop : threading.Event) -> dict[str, str]:
    '''
    Ceci est une fonction permettant de détecter tout les appareils sur le réseau serie
    Elle sortira un dictionnaire de type dict[str, str] = {"SP3": "4F"}\n
    Cette fonction est dérivé de la fonction0x05
    ''' 
    
    # Constantes
    database_modele_hexa: dict[str,str] = {"SP1": "02", "D3": "02", "MR4/dp": "23", "D4": "2e", "DX2-VMS": "3b", "DX4-VMS": "3d", "DXCA": "44", "SP2": "1d", "DX3": "1e", "DX2": "2d", "SP3": "2b", "DX3-VMS": "3c", "DX-VMS-F": "3e", "GS24x8RGB": "3f"}
    fonction : str = "05"
    
    # Variables
    dictionnaire_appareils = {}
    
    # Pour la nomenclature des appareils 
    nombre_objet = 0                                           
    modele_appareil = None
    reponse_appareil = ""


    for i in range(0,256) :
        
        # Permet d'interrompre le script si le flag est True
        if stop.is_set() : 
            return dictionnaire_appareils
        
        # Variables
        test_ping_2_formate = format(i, '02X')

        somme = int(test_ping_2_formate, 16) + int(fonction, 16)

        bcc = format(somme, "02x")[:2]

        print(test_ping_2_formate+fonction+bcc)
        trame = bytes.fromhex(str(test_ping_2_formate + fonction + bcc))
        port_serial.write(trame)

        reponse_appareil = port_serial.read(4)

        if reponse_appareil != "" :
            reponse_modele_appareil = reponse_appareil[2:4]
            for cle, valeur in database_modele_hexa.items() :
                if reponse_modele_appareil != valeur:
                    pass
                else :
                    modele_appareil = cle
                    # Détection de la version de l'objet
                    version_appareil = reponse_appareil[4:6]
                    # 0x1A = 10 (decimal) = version 1.0
                    version_appareil = int(version_appareil, 16)/10

                    dictionnaire_appareils[f"Object_{nombre_objet+1}"] = Appareil(test_ping_2_formate, port_serial, modele_appareil, version_appareil)
                    break

        for x in range(0,256):
            test_ping_4 = format(x, '02X')
            test_ping_4_formate = test_ping_2_formate + test_ping_4

            somme = int(test_ping_4_formate[0:2], 16) + int(test_ping_4_formate[2:4], 16) + int(fonction, 16)

            # Il ce peut que les équipements soit codée de facons à ne jamais avoir une adresse qui pourrait renvoyer un bcc de plus de 1 octet?

            bcc = format(somme, "02x")[:2]

            print(test_ping_4_formate+fonction+bcc)
            trame = bytes.fromhex(test_ping_4_formate + fonction + bcc)
            port_serial.write(trame)
                        
            
            reponse_appareil = port_serial.read(5)

            if reponse_appareil != "" :
                reponse_modele_appareil = reponse_appareil[4:6]
                for cle, valeur in database_modele_hexa.items() :
                    if reponse_modele_appareil != valeur:
                        pass
                    else :
                        modele_appareil = cle
                        # Détection de la version de l'objet
                        version_appareil = reponse_appareil[6:8]
                        # 0x1A = 10 (decimal) = version 1.0
                        version_appareil = int(version_appareil, 16)/10

                        dictionnaire_appareils[f"Object_{nombre_objet+1}"] = Appareil(test_ping_4, port_serial, modele_appareil, version_appareil)
                        break
    return dictionnaire_appareils

############################################################################################################################################################################

# LES FONCTIONS SUIVANTES SONT POUR LA PLUPART UNIQUEMENT UTILISE PAR LE SP3

# Programme l'adresse_appareil de l'appareil
""" def fonction0x00(adresse_appareil) :
    '''
    Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
    Elle sert à programmer la direction de l'appareil ? 
    La trame envoye 3 octets ou 4 selon la longueur de l'adresse 
    La trame reçu est de 1 octet ou 2 selon la longueur de l'adresse 
    '''
    fonction = "00"
    bcc = hex(int(adresse_appareil[0:4], 16) + int(adresse_appareil[2:4], 16)+ int(fonction, 16))[2:]
    trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
    port_serial.write(trame)
    if len(adresse_appareil) == 2 :
        reponse_appareil = port_serial.read(1).hex()     
    else : 
        reponse_appareil = port_serial.read(2).hex()       
    if reponse_appareil == "" :
        raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !") """

# Active ou désactive le mode test du capteur    
def fonction0x01(port_serial, adresse_appareil) :  
    '''
    Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
    Elle sert à activer ou désactiver le mode test du capteur
    A la réception de la trame, si l'appareil est en mode test, il clignotera, si il cesse au bout de quelques secondes il détecte le sol, sinon il ne le détecte pas  
    La trame envoye 4 octets
    La trame reçu est de 2 octets 
    '''
    fonction = "01"
    bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16)+ int(fonction, 16))[2:]
    trame = bytes.fromhex(adresse_appareil + fonction + bcc)
    port_serial.write(trame)
    reponse_appareil = port_serial.read(2).hex()
    if reponse_appareil == "" :
        raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")

# Active / désactive la calibration du potentiomètre 
def fonction0x02(port_serial, adresse_appareil) :
    '''
    Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
    Elle sert à activer ou désactiver la calibration du potentiomètre
    A la réception de la trame, si l'appareil est en état normal, il passera en mode processus d'étalonnage automatique, sinon il arretera immédiatement le mode d'étalonnage et n'enregistra aucun données en mémoire
    La trame envoye 4 octets
    La trame reçu est de 2 octets 
    '''
    fonction = "02"
    bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16)+ int(fonction, 16))[2:] 
    trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
    port_serial.write(trame)
    reponse_appareil = port_serial.read(1).hex()
    if reponse_appareil == "" :
        raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")

# Retourne si l'appareil est en mode reception ou reception/transmission
def fonction0x03(port_serial, adresse_appareil) :
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
    bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16)+ int(fonction, 16))[2:]
    trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
    port_serial.write(trame)
    reponse_appareil = port_serial.read(2).hex()
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
def fonction0x04(port_serial, adresse_appareil) :
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
    reponse_appareil = port_serial.read(2).hex()
    if reponse_appareil == "" :
        raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")
    valeur = int(reponse_appareil[4:6], 16)
    return valeur

# Recherche les informations d'un équipement (Nom de l'équipement | version)
def fonction0x05(port_serial, adresse_appareil: str) -> tuple[str, float]:
    '''
    Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
    Elle sert à retourner le nom de l'équipement ainsi 
    La trame envoye 4 octets
    La trame reçu est de 4 octets
    La fonction retourne une valeur entre 1 à 64 (décimal ou hexa?)
    Réglage de la fréquence de rafraichissement ? ou bien de la sensibilité du capteur
    '''
    fonction = "05"
    nom_appareil = "Nan"
    version_appareil = 0

    dictionnaire_nom_hexa: dict[str,str] = {"SP1": "02", "D3": "02", "MR4/dp": "23", "D4": "2e", "DX2-VMS": "3b", "DX4-VMS": "3d", "DXCA": "44", "SP2": "1d", "DX3": "1e", "DX2": "2d", "SP3": "2b", "DX3-VMS": "3c", "DX-VMS-F": "3e", "GS24x8RGB": "3f"}
    
    if len(adresse_appareil) == 4 :
        somme = int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16)
        
        bcc = format(somme, "02x")[:2]

        trame = bytes.fromhex(adresse_appareil + fonction + bcc)
        port_serial.write(trame)
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
        version_appareil = float(int(version_appareil, 16))/10                                            # 0x0A = 10 (decimal) = version 1.0
        return nom_appareil, version_appareil
            
    elif len(adresse_appareil) == 2 :

        somme = int(adresse_appareil, 16) + int(fonction, 16)

        bcc = format(somme, "02x")[:2]
            
        trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
        port_serial.write(trame)
        reponse_appareil = port_serial.read(4).hex()

        if reponse_appareil == "" :
            raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")   
        
        modele_appareil_hexa = reponse_appareil[2:4]
        for cle, valeur in dictionnaire_nom_hexa.items() :
            if modele_appareil_hexa == valeur:
                nom_appareil = cle
                break

        # Détection de la version de l'objet
        version_appareil = reponse_appareil[6:8]
        version_appareil = int(version_appareil, 16)/10
        return nom_appareil, version_appareil
    else : 
        raise ValueError

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
    limite_superieur = 80 + i * 10 - 1
    if limite_superieur < 400 and reponse_port[4:6] != "15" and reponse_port[4:6] != "16" :
        return limite_superieur

    elif reponse_port[4:6] == "15" :
        return 380
    else : 
        return 400

# Retourne le mode de détection du capteur
def fonction0x07(port_serial, adresse_appareil) :
    '''
    Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
    Elle sert à retourner le mode de détection du capteur
    La trame envoye 4 octets
    La trame reçu est de 4 octets
    La fonction retourne si oui ou non le capteur prend en compte la détection du sol  ?
    '''
    fonction = "07"
    bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16))[2:]
    trame = bytes.fromhex(adresse_appareil + fonction + bcc)
    port_serial.write(trame)
    reponse_port = port_serial.read(2).hex()
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
    reponse_port = port_serial.read(2).hex()
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
    reponse_port = port_serial.read(2).hex()
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
    reponse_port = port_serial.read(2).hex()
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
    reponse_port = port_serial.read(2).hex()
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
        # En mode reception/transmission
        mode_reception_transmission : str = "FF"
    bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16) + int(mode_reception_transmission, 16))[2:]
    trame = bytes.fromhex(adresse_appareil + fonction + mode_reception_transmission + bcc)
    port_serial.write(trame)
    reponse_port = port_serial.read(2).hex()       # Voir si cela ne casse pas qq chose quand enlevé

# Modifie la valeur du potentiomètre digital
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

# Force le capteur à clignoter lorsque le place est libre
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
    reponse_port = port_serial.read(2).hex()       # Voir si cela ne casse pas qq chose quand enlevé

# Force les leds à devenir de couleur verte
def fonction0x19(port_serial, adresse_appareil) :
    fonction = "19"
    bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16))[2:] 
    trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
    port_serial.write(trame)
    reponse_port = port_serial.read(2).hex()       # Voir si cela ne casse pas qq chose quand enlevé

# Force les leds à devenir de couleur rouge
def fonction0x1A(port_serial, adresse_appareil) :
    fonction = "1A"
    bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16))[2:] 
    trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
    port_serial.write(trame)
    reponse_port = port_serial.read(2).hex()       # Voir si cela ne casse pas qq chose quand enlevé

# Force les leds à devenir de couleur orange
def fonction0x1B(port_serial, adresse_appareil) :
    fonction = "1B"
    bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16))[2:] 
    trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
    port_serial.write(trame)
    
    reponse_port = port_serial.read(2).hex()       # Voir si cela ne casse pas qq chose quand enlevé
    return reponse_port

############################################################################################################################################################################

# LES FONCTIONS SUIVANTES SONT POUR LA PLUPART UNIQUEMENT UTILISE PAR LES DX?

# Modifie les chiffres affichés sur l'afficheur
def fonction0x40(port_serial, adresse_appareil, nombre) :
    '''
    Cette fonction à besoin d'un port ouvert donné par la variable port_serial, de l'adresse de l'appareil ainsi qu'une valeur qui sera afficher sur le panneau (compris entre 0 et 10.000)
    Elle sert à modifie la valeur du potentiomètre digital
    La trame envoye 5 octets
    La trame reçu est de 1 octets
    '''
    if nombre < 0 or nombre > 10_000 :
        raise ValueError("Veuillez saisir un nombre compris entre 0 et 10.000")
    
    # Formatage 4 deviendra 0004
    nombre = "{0:04d}".format(int(nombre))
    fonction = "40"
    hexa_nombre_un = hex(ord(nombre[0]))[2:]
    hexa_nombre_deux = hex(ord(nombre[1]))[2:]
    hexa_nombre_trois = hex(ord(nombre[2]))[2:]
    hexa_nombre_quatre = hex(ord(nombre[3]))[2:]
    bcc = hex(int(adresse_appareil, 16) + int(fonction, 16) + int("04", 16) + int(hexa_nombre_un, 16) + int(hexa_nombre_deux, 16) + int(hexa_nombre_trois, 16) + int(hexa_nombre_quatre, 16) )[2:]
    print(str(adresse_appareil + fonction + "04" + hexa_nombre_un + hexa_nombre_deux + hexa_nombre_trois + hexa_nombre_quatre + bcc))
    trame = bytes.fromhex(str(adresse_appareil + fonction + "04" + hexa_nombre_un + hexa_nombre_deux + hexa_nombre_trois + hexa_nombre_quatre + bcc))
    port_serial.write(trame)
    reponse_port = port_serial.read(2).hex()       # Voir si cela ne casse pas qq chose quand enlevé

# Modifie la luminosité des leds 
def fonction0x41(port_serial, adresse_appareil, valeur) :
    '''
    Cette fonction à besoin d'un port ouvert donné par la variable port_serial, de l'adresse de l'appareil ainsi qu'une valeur entre 10 et 250 inclus
    Elle sert à modifier la luminosité des leds des SP3 et DX3
    La trame envoye 3 octets
    La trame reçu est de 3 octets
    '''
    if valeur < 10 or valeur > 250 :
        raise ValueError("Veuillez saisir une valeur entre 10 et 250 !")
    luminosité = hex(int(valeur)) 
    fonction = "41"
    bcc = hex(int(adresse_appareil, 16) + int(fonction, 16) + int("01",16) + int(luminosité, 16))[2:] 
    trame = bytes.fromhex(str(adresse_appareil + fonction + "01" + luminosité + bcc))
    port_serial.write(trame)
    reponse_port = port_serial.read(2).hex()       # Voir si cela ne casse pas qq chose quand enlevé
    
# Affiche la valeur actuelle de la luminosité des leds
def fonction0x42(port_serial, adresse_appareil) :
    '''
    Cette fonction à besoin d'un port ouvert donné par la variable port_serial, de l'adresse de l'appareil
    Elle sert à afficher la valeur actuelle de la luminosité des leds
    La trame envoye 3 octets
    La trame reçu est de 3 octets
    NE SUPPORTE PAS LES SP3 ACTUELLEMENT
    '''
    fonction = "42"
    bcc = hex(int(adresse_appareil, 16) + int(fonction, 16))[2:] 
    trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
    port_serial.write(trame)
    reponse_port = port_serial.read(2).hex()
    if reponse_port == "" : 
        raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")
    valeur = int(reponse_port[2:4], 16)
    return valeur

# Affiche la direction de l'afficheur sur l'afficheur
def fonction0x43(port_serial, adresse_appareil) :
    '''
    Cette fonction à besoin d'un port ouvert donné par la variable port_seriale et de l'adresse de l'appareil
    Elle sert à afficher la valeur actuelle de la luminosité des leds
    La trame envoye 3 octets
    La trame reçu est de 1 octets
    '''
    fonction = "43"
    bcc = hex(int(adresse_appareil, 16) + int(fonction, 16))[2:] 
    trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
    port_serial.write(trame)
    reponse_port = port_serial.read(1).hex()
    if reponse_port == "" : 
        raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")


# Modifie le type de caractère à partir de zero?
def fonction0x4B(port_serial, adresse_appareil) :
        fonction = "4B"
        bcc = hex(int(adresse_appareil, 16) + int(fonction, 16) + int(1))[2:]                      # Fabrication du byte verifiant la somme de tous les octets précédent, verifiant ainsi l'intégrité de la trame 
        trame = bytes.fromhex(str(adresse_appareil + fonction + "01" + bcc))
        port_serial.write(trame)
        reponse_port = port_serial.read(2).hex()

# Modifie le sens haut/bas de l'afficheur
def fonction0x49(port_serial, adresse_appareil, direction : bool) :
    '''
    Cette fonction à besoin d'un port ouvert donné par la variable port_serial, de l'adresse de l'appareil ainsi qu'une booléenne True : vers le haut , False : vers le bas 
    Elle sert à modifier le sens haut/bas de l'afficheur
    La trame envoye 4 octets
    La trame reçu est de 1 octet
    '''
    fonction = "49"
    if direction == True : 
        direction_hexa = "01"
    else : 
        direction_hexa = "00"

    bcc = hex(int(adresse_appareil, 16) + int(fonction, 16) + int(direction_hexa))[2:]
    trame = bytes.fromhex(str(adresse_appareil + fonction + direction_hexa + bcc))
    port_serial.write(trame)
    reponse_port = port_serial.read(2).hex()    # Voir si ça ne casse pas le script
'''
 # Script combo capteur / display 
if __name__ == "__main__" :
    
    port, baudrate, timeout, port_serial = test_port_ouvert()

    with port_serial :
        # Variables
        nom_appareil_SP3 : str
        nom_appareil_DX3 : str
        compteur_voiture : int = 0

        # Obtenir les adresses des appareils 
        nom_appareil_SP3 = input("Veuillez saisir l'adresse du SP3 : ")
        nom_appareil_DX3 = input("Veuillez saisir l'adresse du DX3 : ")

        print(fonction0x05(port_serial, nom_appareil_SP3))

        # Si une place est disponible mettre 1 sur l'afficheur sinon non
        try:
            while True: 
                if fonction0x10(port_serial, nom_appareil_SP3) == True :
                    compteur_voiture = 1
                    fonction0x40(port_serial, nom_appareil_DX3, compteur_voiture)
                else : 
                    compteur_voiture = 0
                    fonction0x40(port_serial, nom_appareil_DX3, compteur_voiture) 
        except KeyboardInterrupt :
            pass
            
        port_serial.close()

'''

if __name__ == "__main__" :

    port, baudrate, timeout, port_serial = test_port_ouvert()
    with port_serial :
        print(fonction0x1B(port_serial, "1B53"))
        sleep(1)
        fonction0x1A(port_serial, "1B53")
        sleep(1)
        fonction0x19(port_serial, "1B53")
        print("a")