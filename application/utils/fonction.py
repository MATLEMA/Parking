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