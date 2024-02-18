#from .SP3 import SP3
#from .DX3 import DX3
from threading import Thread, Event
from time import sleep

class Parking:
    def __init__(self, liste_SP3: list, liste_DX3: list) -> None:
        self.liste_SP3: list = liste_SP3
        self.places_libre_SP3: dict = {}
        self.liste_DX3: list = liste_DX3
        self.stop = Event()

        self.thread_place_libre = Thread(target=self.gestion_places_libre)
        self.thread_place_libre.start()

        sleep(1)

        self.thread_gestion_affichage = Thread(target=self.gestion_affichage)
        self.thread_gestion_affichage.start()

    def gestion_places_libre(self):
        
        while not self.stop.is_set():
            for i in self.liste_SP3:
                self.places_libre_SP3[i] = i.place_libre()
            sleep(3)

    def gestion_affichage(self):
        
        while not self.stop.is_set():
            compteur: int = 0
            for valeur in self.places_libre_SP3:
                if valeur == True:
                    compteur += 1
            
            # TODO
            self.liste_DX3[0].afficheur(str(compteur))
            sleep(3)

    def stop_threads(self):
        self.stop.set()
        self.thread_gestion_affichage.join()
        self.thread_place_libre.join()