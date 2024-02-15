from serial import Serial
# Permet de mettre le dispositif en mode programmation 4F
trame_envoyee: bytes = bytes.fromhex("4fDB12")

with Serial("/dev/ttyUSB0", 19200, timeout= 1) as port_serial:
    while True:
        port_serial.write(trame_envoyee)
        trame_reponse: bytes = port_serial.read()
        print(trame_reponse)


trame_envoyee: bytes = bytes.fromhex("1b53DB14")

with Serial("/dev/ttyUSB0", 19200, timeout= 1) as port_serial:
    while True:
        port_serial.write(trame_envoyee)
        trame_reponse: bytes = port_serial.read()
        print(trame_reponse)


