from serial import Serial, SerialException, tools
import serial.tools.list_ports

# Teste si le port est ouvert 
def connecter(port, baudrate, timeout):
    baudrate = int(baudrate)
    timeout = float(timeout)

    try :
        Serial(port, baudrate, timeout= timeout)
        return True
    except SerialException :
        return False
    
# Liste les port sur la machine
def listing_port()  -> list[str]:
    dictionnaire_port : list[str] = []
    listing_des_ports = serial.tools.list_ports.comports()                                      # Création d'une liste sous forme de class ListPortInfo

    # Boucle qui passe par tout les paramètres de la class ListPortInfo de notre variable listing_des_ports
    for information_port_disponible in listing_des_ports :
        dictionnaire_port.append(information_port_disponible.device)
    return dictionnaire_port

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