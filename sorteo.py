import random

jugadas = int(input("numero de jugadas:"))
numero_ganadores = int(jugadas*0.134)
lista_jugadas = []
lista_ganadores = []
i = 0
"""
    este ciclo es sólo para llenar la lista
    en este caso de prueba
"""
if jugadas == 1000:
    for i in range(0, 1000):
        lista_jugadas.append(i)
else:
    while i < jugadas:
        numero = random.randint(0, 999)
        if lista_jugadas.count(numero) > 0:
            continue
        else:
            lista_jugadas.append(numero)
            i += 1
lista_jugadas.sort()
print(lista_jugadas)
"""
    este si es para seleccionar los ganadores. La idea es importar de models.Jugada, los objectos que tengan
    status='pagado' en una lista (lista_jugadas). Puedo hacer una clase con todo esto metido, y cuando vaya a
    sortear hago una instancia de la clase, pasándole al constructor de la clase la lista_jugadas.
        sort = Sorteo(lista_jugadas)
        sort.sortear()
        sort.primero
        sort.segundo
        [...]
        sort.lista_repechaje
"""
i = 0
true_random = random.SystemRandom()
while i < numero_ganadores:
    posicion_lista = true_random.randint(0, (jugadas-1))
    ganador = lista_jugadas[posicion_lista]
    if lista_ganadores.count(ganador) > 0:
        continue
    else:
        lista_ganadores.append(ganador)
        i += 1
print(lista_ganadores)
gold = int((numero_ganadores-3)*0.07)
silver = int((numero_ganadores-3)*0.15)
bronze = int((numero_ganadores-3)*0.26)
repechaje = int((numero_ganadores-3)*0.52)
repechaje += numero_ganadores-3-gold-silver-bronze-repechaje
lista_gold = lista_ganadores[3:(3+gold)]
lista_silver = lista_ganadores[(3+gold):(3+gold+silver)]
lista_broze = lista_ganadores[(3+gold+silver):(3+gold+silver+bronze)]
lista_repechaje = lista_ganadores[(3+gold+silver+bronze):]
print("1er lugar: ", lista_ganadores[0])
print("2do lugar: ", lista_ganadores[1])
print("3er lugar: ", lista_ganadores[2])
print("Grupo Gold (%d):\n" % gold, lista_gold)
print("Grupo Silver(%d):\n" % silver, lista_silver)
print("Grupo Bronze (%d):\n" % bronze, lista_broze)
print("Grupo Repechaje(%d):\n" % repechaje, lista_repechaje)