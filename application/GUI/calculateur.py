from tkinter import Frame, Tk, Button,ttk
from serial import Serial
from utils import SP3, DX3
from threading import Thread
from time import sleep

class Launch(Frame):

    def __init__(self, parent: Tk, port: Serial, adresse_afficheur: DX3) -> None:
        super().__init__(parent)

        self.port: Serial = port
        self.parent: Tk = parent
        self.adresse_afficheur: DX3 = adresse_afficheur
        bouton_demarrer = ttk.Button(self, text="Demarrer", command=self.thread)
        bouton_demarrer.pack()

    def demarrer(self):
        self.thread_gestion_affichage = Thread(target=self.thread)
        self.thread_gestion_affichage.start() 

    def thread(self) -> None:
        while True:
            nombre_place = str(sum(SP3.place_libre(self.port)))
            print(nombre_place)
            sleep(2)

            self.adresse_afficheur.afficheur(nombre_place)
