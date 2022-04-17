def verteile_aufgaben(bereich):
    return [[i, i + (bereich[1] - bereich[0])//11, i//((bereich[1] - bereich[0])//11)] for i in range(bereich[0], bereich[1], (bereich[1] - bereich[0])//11)]


print(verteile_aufgaben([0, 220]))
