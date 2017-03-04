import random


class Sorteo(object):

    def __init__(self, cant_jugadas, lista_jugadas):

        self.jugadas = cant_jugadas
        self.numero_ganadores = int(self.jugadas*0.134)
        self.lista_jugadas = lista_jugadas
        self.lista_ganadores = []
        self.primero = None
        self.segundo = None
        self.tercero = None
        self.lista_gold = []
        self.lista_silver = []
        self.lista_bronze = []
        self.lista_repechaje = []

    """
        este es el metodo para seleccionar los ganadores. La idea es importar de models.Jugada, los objectos que tengan
        status='pagado' en una lista (lista_jugadas). Puedo hacer una clase con todo esto metido, y cuando vaya a
        sortear hago una instancia de la clase, pasándole al constructor de la clase la lista_jugadas.
            sort = Sorteo(lista_jugadas)
            sort.sortear()
            sort.primero
            sort.segundo
            [...]
            sort.lista_repechaje
    """
    def sortear(self):
        i = 0
        true_random = random.SystemRandom()
        while i < self.numero_ganadores:
            posicion_lista = true_random.randint(0, (self.jugadas-1))
            ganador = self.lista_jugadas[posicion_lista]
            if self.lista_ganadores.count(ganador) > 0:
                continue
            else:
                self.lista_ganadores.append(ganador)
                i += 1
        self.primero = self.lista_ganadores[0]
        self.segundo = self.lista_ganadores[1]
        self.tercero = self.lista_ganadores[2]
        gold = int((self.numero_ganadores-3)*0.07)
        silver = int((self.numero_ganadores-3)*0.15)
        bronze = int((self.numero_ganadores-3)*0.26)
        repechaje = int((self.numero_ganadores-3)*0.52)
        repechaje += self.numero_ganadores-3-gold-silver-bronze-repechaje
        self.lista_gold = self.lista_ganadores[3:(3+gold)]
        self.lista_silver = self.lista_ganadores[(3+gold):(3+gold+silver)]
        self.lista_bronze = self.lista_ganadores[(3+gold+silver):(3+gold+silver+bronze)]
        self.lista_repechaje = self.lista_ganadores[(3+gold+silver+bronze):]