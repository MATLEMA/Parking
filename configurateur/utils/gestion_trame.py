from serial import Serial

def calcul_bcc(adresse_appareil: str, nom_fonction : str, valeur = "")   -> str :
    """Calcul la somme des octets en 1 octet

    :param adresse_appareil: adresse hexadécimal d'un appareil
    :type adresse_appareil: str
    :param nom_fonction: Nom de la fonction 
    :type nom_fonction: str
    :param valeur: valeur optionnel à ajouter si la fonction en a besoin, defaults to ""
    :type valeur: str, optional
    :raises ValueError: adresse_appareil en hexadécimal
    :raises ValueError: adresse_appareil doit être de longeur 2 ou 4!
    :return: Somme de tout les octets en un seul octet 
    :rtype: str
    """
    # Vérifie si adresse_appareil est valide avant tout calcul
    try :
        int(adresse_appareil, 16)
    except ValueError :
        raise ValueError("Adresse_appareil en hexadecimal!")

    if len(adresse_appareil) == 4 :

        if valeur == "" :
            somme = int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(nom_fonction, 16) 
        else : 
            somme = int(adresse_appareil[0:2], 16) + int(adresse_appareil[2:4], 16) + int(nom_fonction, 16)
            for i in range(0, len(valeur), 2):
                somme += int(valeur[i:i+2], 16)

        bcc = format(somme, "02x")[-2:]

        return bcc

    elif len(adresse_appareil) == 2 :

        if valeur == "" :
            somme = int(adresse_appareil, 16) + int(nom_fonction, 16)
        else : 
            somme = int(adresse_appareil, 16) + int(nom_fonction, 16)
            for i in range(0, len(valeur), 2):
                somme += int(valeur[i:i+2], 16)
            
        bcc = format(somme, "02x")[-2:]

        return bcc
    
    else :
        raise ValueError("Adresse_appareil doit être de longeur 2 ou 4!")

def envoi_trame(port_serial: Serial, adresse_appareil : str, nom_fonction: str, retry : int, valeur: str = "") -> str :
    """Envoie un trame sur le port serial renseigné

    :param port_serial: Port COM 
    :type port_serial: Serial
    :param adresse_appareil: adresse hexadécimal d'un appareil
    :type adresse_appareil: str
    :param nom_fonction: Nom de la fonction 
    :type nom_fonction: str
    :param bcc: Somme de tout les octets en un seul octet 
    :type bcc: str
    :param retry: Nombre d'essaie si le module echoue
    :type retry: int
    :param valeur: valeur optionnel à ajouter si la fonction en a besoin, defaults to ""
    :type valeur: str, optional
    :raises TimeoutError: L'appareil n'a pas répondu
    :return: retourne la trame réponse en hexadécimal
    :rtype: str
    """    

    bcc = calcul_bcc(adresse_appareil, nom_fonction, valeur)
    while retry > 0 :
        # Fabrication de la trame à envoyée

        if valeur != "":
            valeur= format(valeur, "02")

        trame_envoyee: bytes = bytes.fromhex(adresse_appareil + nom_fonction + valeur + bcc)

        print(adresse_appareil + nom_fonction + valeur + bcc)

        # Envoie de la trame 
        port_serial.write(trame_envoyee)

        # Reception de la réponse 
        trame_reponse = port_serial.read(10)
        trame_reponse = trame_reponse.hex()

        if verification_validite_trame(adresse_appareil, trame_reponse) :
            return trame_reponse
        else :
            retry -= 1
    raise TimeoutError("L'appareil n'a pas répondu")

def verification_validite_trame(adresse_appareil: str, trame_recu: str) -> bool:
    '''
    Une trame réponse :
    <adr>
    <adrh><adrl>
    <adr><reg><~bcc>
    <adr><~bcc>
    '''

    adresse = adresse_appareil
    longueur_adresse = len(adresse_appareil)
    longueur_trame = len(trame_recu)
    trame_a_traite = trame_recu[:2] # On enleve le bcc
    bcc_recu = trame_recu[-2:]      # On garde le bcc
    somme = 0

    # Test
    if trame_recu != "":
        print(f"Trame recu : {trame_recu}")
    # La validité s'effectue en vérifiant uniquement si la longueur de la trame == la longueur de l'adresse pour deux cas 
    # <adr>
    # <adrh><adrl>
    if longueur_adresse == longueur_trame:
        return adresse == trame_recu
    # La validité s'effectue en vérifiant uniquement si la longueur de la trame > longueur de l'adresse pour tout les autres cas
    # <adr><reg><~bcc>
    # <adr><~bcc>
    else:
        for i in range(0, len(trame_a_traite), 2):
            somme += int(trame_a_traite[i:i+2], 16)
        
        # Complément à un (inversion des 0 et des 1)
        bcc = hex(int(hex(somme), 16) ^ 0xFF)[2:]
        return bcc_recu == bcc