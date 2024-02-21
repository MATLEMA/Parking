from serial import Serial
# Permet de lire la direction des numéros 00 ou 01
trame_envoyee: bytes = bytes.fromhex("4f40043035353516")

with Serial("/dev/ttyUSB0", 19200, timeout= 1) as port_serial:
    while True:
        port_serial.write(trame_envoyee)
        trame_reponse: bytes = port_serial.read()
        print(trame_reponse)
