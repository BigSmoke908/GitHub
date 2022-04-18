import importlib


def verteile_aufgaben(bereich, anzahl=11):
    return [[i, i + (bereich[1] - bereich[0])//anzahl, i//((bereich[1] - bereich[0])//anzahl)] for i in range(bereich[0], bereich[1], (bereich[1] - bereich[0])//anzahl)]


def maxima(eingabe):
    return max([max(liste) for liste in eingabe])


z = -1.2455454294460577e+154+1.055979384095098e+154j
print(z ** 2)
print(z.real ** 2 + z.imag ** 2 > 4)
