def verteile_aufgaben(bereich, anzahl=11):
    return [[i, i + (bereich[1] - bereich[0])//anzahl, i//((bereich[1] - bereich[0])//anzahl)] for i in range(bereich[0], bereich[1], (bereich[1] - bereich[0])//anzahl)]


def maxima(eingabe):
    return max([max(liste) for liste in eingabe])


print(verteile_aufgaben([0, 2160], 12))
