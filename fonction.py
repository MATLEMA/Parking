import serial
import serial.tools.list_ports
import sys
import math
import ma_class

# Variables : 
port : str                              # Dossier du port COM sélectionné
baudrate : int                          # Baudrate
timeout : float                         # Timeout port

# Listing des ports // Doit marcher sur linux et windows !! 

listing_des_ports = serial.tools.list_ports.comports()                                                                                                   # Création d'une liste sous forme de class ListPortInfo
print(f"Nom   Description\n")          

# Boucle qui passe par tout les paramètres de la class ListPortInfo de notre variable listing_des_ports
for information_port_disponible in (listing_des_ports) :
    print(f"{information_port_disponible.device} | {information_port_disponible.description} | {information_port_disponible.interface}\n")


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
            port = str(input("Veuillez l'adresse du port : "))
            break
        except ValueError : 
            print("*Erreur type : Valeur ")

    # Boucle pour l'adressage du baudrate
    while True :
        list_baudrate_possible = [4800,9600,19200] 
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
        port_serial = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        print(f"Le port {port} est ouvert ! ")
        break
    except serial.SerialException :
        print(f"Le port {port} n'est pas ouvert réessayer avec un autre port ou verifier votre installation !")

# Détection automatique de tous les appareils connectés en réseau serie
def detection_appareil() :
    '''
    Ceci est une fonction permettant de détecter tout les appareils sur le réseau serie
    Elle ne prend rien en entrée
    Elle sortira un dictionnaire de type dict[str, str] = {"SP3": "4F"}\n
    Cette fonction est EXTREMEMENT LOURDE pour le reseau 
    Il lui faudra au minimum 200s 65535*3*10^-3= 196s
    Cette fonction est dérivé de la fonction0x05
    '''
    # Constantes
    dictionnaire_nom_hexa: dict[str,str] = {"SP1": "02", "D3": "02", "MR4/dp": "0x23", "D4": "0x2E", "DX2-VMS": "0x3B", "DX4-VMS": "0x3D", "DXCA": "0x44", "SP2": "0x1D", "DX3": "0x1E", "DX2": "0x2D", "SP3": "0x2B", "DX3-VMS": "0x3C", "DX-VMS-F": "0x3E", "GS24x8RGB": "0x3F"}
    fonction = "05"
    
    # Variables
    dictionnaire_appareils : dict[str, str] = {}
    nombre_appareil = 1
    modele_appareil =None

    for i in range(0,256) :

        # Variables
        test_ping = hex(i)[2:]

        bcc = hex(int(test_ping, 16) + int(fonction, 16))[2:]
        trame = bytes.fromhex(str(test_ping + fonction + bcc))
        port_serial.write(trame)
        reponse_appareil = port_serial.read(4).hex()
        if reponse_appareil == "" :
            continue
        else : 
            modele_appareil_hexa = reponse_appareil[2:4]   
            for cle, valeur in dictionnaire_nom_hexa.items() :
                if modele_appareil_hexa == valeur:
                    modele_appareil= cle
                    nombre_appareil += 1
                    break
                
            # Détection de la version de l'objet
            if modele_appareil is not None :
                version_appareil = reponse_appareil[4:6]
                version_appareil = int(version_appareil, 16)/10                                            # 0x1A = 10 (decimal) = version 1.0
                nouvel_appareil = ma_class.Appareil(port, modele_appareil, version_appareil, test_ping)
                dictionnaire_appareils[nouvel_appareil.modele] = str(test_ping)

        for x in range(0,256):
            test_ping_4 = test_ping + hex(x)[2:]
            bcc = hex(int(test_ping_4[0:2], 16) + int(test_ping_4[2:4], 16) + int(fonction, 16))[2:]
            trame = bytes.fromhex(str(test_ping_4 + fonction + bcc))
            port_serial.write(trame)
            reponse_appareil = port_serial.read(5).hex()
            if reponse_appareil == "" :
                continue
            else :  
                modele_appareil_hexa = reponse_appareil[4:6]   
                for cle, valeur in dictionnaire_nom_hexa.items() :
                    if modele_appareil_hexa == valeur:
                        modele_appareil= cle
                        nombre_appareil += 1
                        break
                
            # Détection de la version de l'objet
            if modele_appareil is not None :
                version_appareil = reponse_appareil[6:8]
                version_appareil = int(version_appareil, 16)/10                                            # 0x1A = 10 (decimal) = version 1.0
                nouvel_appareil = ma_class.Appareil(port, modele_appareil, version_appareil, test_ping_4)
                dictionnaire_appareils[nouvel_appareil.modele] = str(test_ping_4)

    return dictionnaire_appareils

# Programme l'adresse_appareil de l'appareil
def fonction0x00(adresse_appareil) :
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
        raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")

# Active ou désactive le mode test du capteur    
def fonction0x01(adresse_appareil) :  
    '''
    Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
    Elle sert à activer ou désactiver le mode test du capteur
    A la réception de la trame, si l'appareil est en mode test, il clignotera, si il cesse au bout de quelques secondes il détecte le sol, sinon il ne le détecte pas  
    La trame envoye 4 octets
    La trame reçu est de 2 octets 
    '''
    fonction = "01"
    bcc = hex(int(adresse_appareil[0:4], 16) + int(adresse_appareil[2:4], 16)+ int(fonction, 16))[2:]
    trame = bytes.fromhex(adresse_appareil + fonction + bcc)
    port_serial.write(trame)
    reponse_appareil = port_serial.read(2).hex()
    if reponse_appareil == "" :
        raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")

# Active / désactive la calibration du potentiomètre 
def fonction0x02(adresse_appareil) :
    '''
    Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
    Elle sert à activer ou désactiver la calibration du potentiomètre
    A la réception de la trame, si l'appareil est en état normal, il passera en mode processus d'étalonnage automatique, sinon il arretera immédiatement le mode d'étalonnage et n'enregistra aucun données en mémoire
    La trame envoye 4 octets
    La trame reçu est de 2 octets 
    '''
    fonction = "02"
    bcc = hex(int(adresse_appareil[0:4], 16) + int(adresse_appareil[2:4], 16)+ int(fonction, 16))[2:] 
    trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
    port_serial.write(trame)
    reponse_appareil = port_serial.read(2).hex()
    if reponse_appareil == "" :
        raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")

# Retourne si l'appareil est en mode reception ou reception/transmission
def fonction0x03(adresse_appareil) :
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
    bcc = hex(int(adresse_appareil[0:4], 16) + int(adresse_appareil[2:4], 16)+ int(fonction, 16))[2:]
    trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
    port_serial.write(trame)
    reponse_appareil = port_serial.read(4).hex()
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
def fonction0x04(adresse_appareil) :
    '''
    Cette fonction à besoin d'un port ouvert donné par la variable port_serial ainsi que l'adresse_appareil
    Elle sert à retourner la valeur du potentiomètre digital
    La trame envoye 4 octets
    La trame reçu est de 4 octets
    La fonction retourne une valeur entre 1 à 64 (décimal ou hexa?)
    Réglage de la fréquence de rafraichissement ? ou bien de la sensibilité du capteur

    '''
    fonction = "04"
    bcc = hex(int(adresse_appareil[0:4], 16) + int(adresse_appareil[2:4], 16)+ int(fonction, 16))[2:]
    trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
    port_serial.write(trame)
    reponse_appareil = port_serial.read(4).hex()
    if reponse_appareil == "" :
        raise NameError("L'appareil n'a pas répondu :( vérifier votre installation ou l'adresse donnée !")
    valeur = int(reponse_appareil[4:6], 16)
    return valeur

# Recherche les informations d'un équipement (Nom de l'équipement | version)
def fonction0x05(adresse_appareil) :
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
        return nom_appareil, version_appareil
            
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
        return nom_appareil, version_appareil 

    else : 
        sys.exit("Il y a eu une erreur !")

def fonction0x06(adresse_appareil) :                                                            # Retourne la distance de détection maximal du capteur
        fonction = "06"
        bcc = hex(int(adresse_appareil, 16) + int(fonction, 16))                      # Fabrication du byte verifiant la somme de tous les octets précédent, verifiant ainsi l'intégrité de la trame 
        trame = bytes.fromhex(adresse_appareil + fonction + bcc)
        port_serial.write(trame)
        reponse_port = port_serial.read(4).hex()          # Lecture du port sur 4 octet en ascii puis en hexa

        i = int(reponse_port[4:6], 16)
        limite_inferieur = 70 + i * 10
        limite_superieur = 80 + i * 10 - 1
        if limite_superieur < 400 and reponse_port[4:6] != "15" and reponse_port[4:6] != "16" :
            print(f"La distance de détection est entre {limite_inferieur} et {limite_superieur} cm")

        elif reponse_port[4:6] == "15" :
            print(f"La distance de détection est entre 380 et 399 cm")
        else : 
            print(f"La distance de détection est au dessus de 400 cm")

def fonction0x07(adresse_appareil) :                                                            # Retourne le mode de détection du capteur
        fonction = "07"
        bcc = hex(int(adresse_appareil, 16) + int(fonction, 16))                      # Fabrication du byte verifiant la somme de tous les octets précédent, verifiant ainsi l'intégrité de la trame 
        trame = bytes.fromhex(adresse_appareil + fonction + bcc)
        port_serial.write(trame)
        reponse_port = port_serial.read(4).hex()          # Lecture du port sur 2 octet en ascii
        if reponse_port[4:6] == "00" :
            print("L'appareil prendra en compte la détection du sol pour décider de son état")
        else :
            print("L'appareil ne prendra pas en compte la détection du sol pour décider de son état")

def fonction0x09(adresse_appareil) :                                                            # Retourne le mode de détection du capteur
        fonction = "09"
        bcc = hex(int(adresse_appareil, 16) + int(fonction, 16))                      # Fabrication du byte verifiant la somme de tous les octets précédent, verifiant ainsi l'intégrité de la trame 
        trame = bytes.fromhex(adresse_appareil + fonction + bcc)
        port_serial.write(trame)
        reponse_port = port_serial.read(4).hex()          # Lecture du port sur 2 octet en ascii
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

def fonction0x10(adresse_appareil) :                                                            # Renvoie si la place est libre ou non 
        fonction = "10"
        bcc = hex(int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(fonction, 16))[2:] 
        print(bcc)                # Fabrication du byte verifiant la somme de tous les octets précédent, verifiant ainsi l'intégrité de la trame 
        trame = bytes.fromhex(str(adresse_appareil + fonction + bcc))
        print(bytes.fromhex(fonction))
        print(trame)
        port_serial.write(trame)
        reponse_port = port_serial.read(4).hex()          # Lecture du port sur 4 octet en ascii
        print(reponse_port)
        if reponse_port[4:6] == "00":
            is_open = True
        else : 
            is_open = False
        return is_open

def fonction0x11(adresse_appareil) :                                                            # Modifie la distance maximal de detection
            fonction = "11"
            while True :
                try:
                    while True : 
                        distance = int(input("Veuillez saisir la distance maximal de détection du capteur (min 150cm, max 400cm): "), 10)
                        if distance < 150 :
                            print("Veuillez saisir un nombre superieur à 150cm")
                            pass
                        else :
                            break
                    break
                except ValueError:
                    print("Veuillez saisir un nombre superieur à 150cm")
            distance = distance//10 * 10
            distance = hex(distance)[2:]
            




            bcc = hex(int(adresse_appareil, 16) + int(fonction, 16))                      # Fabrication du byte verifiant la somme de tous les octets précédent, verifiant ainsi l'intégrité de la trame 
            trame = bytes.fromhex(adresse_appareil + fonction + distance + bcc)
            port_serial.write(trame)
            reponse_port = port_serial.read(4).hex()          # Lecture du port sur 4 octet en ascii puis en hexa

def fonction0x1B(adresse_appareil) :                                                            # LED capteur libre en Orange
        trame = bytes.fromhex('1B531B89')           # Conversion hexa en octets
        port_serial.write(trame)
        reponse_port = port_serial.read(2)          # Lecture du port sur 2 octet en ascii
        reponse_port = reponse_port.hex()           # Conversion octets en hexa
        return reponse_port
        
def fonction0x1A(adresse_appareil) :                                                            # LED capteur libre en Rouge
        trame = bytes.fromhex('1B531A88')           # Conversion hexa en octets
        port_serial.write(trame)
        reponse_port = port_serial.read(2)          # Lecture du port sur 2 octet en ascii
        reponse_port = reponse_port.hex()           # Conversion octets en hexa
        return reponse_port
        
def fonction0x19(adresse_appareil) :                                                            # LED capteur libre en Vert
        trame = bytes.fromhex('1B531987')           # Conversion hexa en octets
        port_serial.write(trame)
        reponse_port = port_serial.read(2)          # Lecture du port sur 2 octet en ascii
        reponse_port = reponse_port.hex()           # Conversion octets en hexa
        return reponse_port 
    
######################################################################################################################

def fonction0x4B(adresse_appareil) :                                                            # Modifier le sens d'affichage
        fonction = "4B"
        bcc = hex(int(adresse_appareil, 16) + int(fonction, 16) + int(1))[2:]                      # Fabrication du byte verifiant la somme de tous les octets précédent, verifiant ainsi l'intégrité de la trame 
        trame = bytes.fromhex(str(adresse_appareil + fonction + "01" + bcc))
        port_serial.write(trame)
        reponse_port = port_serial.read(2).hex()

def fonction0x49(adresse_appareil) :                                                            # Modifier le sens d'affichage
        fonction = "49"
        bcc = hex(int(adresse_appareil, 16) + int(fonction, 16) + int(1))[2:]                      # Fabrication du byte verifiant la somme de tous les octets précédent, verifiant ainsi l'intégrité de la trame 
        trame = bytes.fromhex(str(adresse_appareil + fonction + "01" + bcc))
        port_serial.write(trame)
        reponse_port = port_serial.read(2).hex()


