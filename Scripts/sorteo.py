import random


class Sorteo(object):

    def __init__(self, cant_jugadas, lista_jugadas):

        self.jugadas = int(cant_jugadas)
        if self.jugadas > 134:
            self.numero_ganadores = int(self.jugadas*0.134)
        else:
            if 2 < self.jugadas < 4:
                self.numero_ganadores = 1
            elif 4 <= self.jugadas <= 20:
                self.numero_ganadores = 2
            elif 21 <= self.jugadas <= 129:
                if self.jugadas % 10 == 0:
                    self.numero_ganadores = self.jugadas / 10
                else:
                    self.numero_ganadores = int(self.jugadas/10) + 1
            else:
                self.numero_ganadores = 13

        self.lista_jugadas = lista_jugadas
        self.lista_ganadores = []
        self.primero = None
        self.segundo = None
        self.tercero = None
        self.gold = None
        self.silver = None
        self.bronze = None
        self.repechaje = None
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

        if self.numero_ganadores > 1:
            self.segundo = self.lista_ganadores[1]
        if self.numero_ganadores > 2:
            self.tercero = self.lista_ganadores[2]
        if self.numero_ganadores > 3 and self.jugadas < 135:
            self.lista_gold.append(self.lista_ganadores[3])
        if self.numero_ganadores > 4 and self.jugadas < 135:
            self.lista_silver.append(self.lista_ganadores[4])
        if self.numero_ganadores > 5 and self.jugadas < 135:
            self.lista_bronze.append(self.lista_ganadores[5])
        if self.numero_ganadores > 6 and self.jugadas < 135:
            self.lista_repechaje.append(self.lista_ganadores[6])
        if self.numero_ganadores > 7 and self.jugadas < 135:
            self.lista_repechaje.append(self.lista_ganadores[-1])
        if self.numero_ganadores > 8 and self.jugadas < 135:
            self.lista_repechaje.append(self.lista_ganadores[-2])
        if self.numero_ganadores > 9 and self.jugadas < 135:
            self.lista_bronze.append(self.lista_ganadores[-3])
        if self.numero_ganadores > 10 and self.jugadas < 135:
            self.lista_bronze.append(self.lista_ganadores[-4])
        if self.numero_ganadores > 11 and self.jugadas < 135:
            self.lista_silver.append(self.lista_ganadores[-5])
        if self.numero_ganadores > 12 and self.jugadas < 135:
            self.lista_repechaje.append(self.lista_ganadores[-6])

        if self.jugadas >= 135:
            self.gold = int((self.numero_ganadores-3)*0.07)
            self.silver = int((self.numero_ganadores-3)*0.15)
            self.bronze = int((self.numero_ganadores-3)*0.26)
            self.repechaje = int((self.numero_ganadores-3)*0.52)
            self.repechaje += self.numero_ganadores-3-self.gold-self.silver-self.bronze-self.repechaje
            self.lista_gold = self.lista_ganadores[3:(3+self.gold)]
            self.lista_silver = self.lista_ganadores[(3+self.gold):(3+self.gold+self.silver)]
            self.lista_bronze = self.lista_ganadores[(3+self.gold+self.silver):(3+self.gold+self.silver+self.bronze)]
            self.lista_repechaje = self.lista_ganadores[(3+self.gold+self.silver+self.bronze):]

"""
n = int(input())
lista = []
i = 0
true_random = random.SystemRandom()
while i < n:
    r = true_random.randint(0, 1000)
    if lista.count(r) > 0:
        continue
    else:
        lista.append(r)
        i += 1
lista.sort()
print(lista)
s = Sorteo(n, lista)
s.sortear()

print(s.numero_ganadores, s.jugadas)
print(s.lista_ganadores)
print(s.primero)
print(s.segundo)
print(s.tercero)
print(s.lista_gold)
print(s.lista_silver)
print(s.lista_bronze)
print(s.lista_repechaje)
"""
