class Appareil:
        def __init__(self ,port_serial : str, modele : str ,version: float, adresse: str) :
            self.port_serial = port_serial
            self.modele = modele
            self.version = version
            self.adresse = adresse