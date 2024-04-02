from serial import Serial
from time import sleep
# Permet de lire la direction des numéros 00 ou 01
trame_envoyee_1: bytes = bytes.fromhex("1b53016f")
trame_envoyee_2: bytes = bytes.fromhex("4f40043035353516")

with Serial("/dev/ttyUSB0", 19200, timeout= 1) as port_serial:
    port_serial.write(trame_envoyee_1)
    trame_reponse: bytes = port_serial.read()
    print(f"Réponse 1 : {trame_reponse}")




# { 2c 40 04 30 30 31 35 36 => 2c } OK 
# bcc = 136