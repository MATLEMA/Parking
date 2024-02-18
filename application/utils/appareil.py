from serial import Serial

class Appareil:
    def __init__(self, adresse: str, port_serial : Serial, modele : str) :
        self.port_serial = port_serial
        self.modele = modele
        self.adresse = adresse