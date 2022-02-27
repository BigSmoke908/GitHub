import math
import random
import sys
from PIL import Image
import time
import matplotlib.pyplot as plt
import numpy as np
from functools import partial
from multiprocessing import Pool
from copy import deepcopy as copy


# X/Y sind die Seitenlängen von der Heightmap, noises ist eine list mit den verschiedenen Stufen von Noise die
# übereinandergelegt werden sollen um die Heightmap zu generieren
def generate_heightmap(x, y, noises):
    return [[0 for i in range(x)] for j in range(y)]


# generiert Noise mit den Maßen X/Y und fügt so viele Highpoints hinzu wie angegeben (Punkte die die maximale Höhe haben)
# (highpoints = wie viele Punkte es gibt, die die maximale Höhe haben)
def generate_noise(x, y, highpoints):
    return [[0 for i in range(x)] for j in range(y)]


# (partsize = wie viele Zeilen von jedem einzelnen Prozess geglättet werden sollen,
# etwa ein Zwölftel der Kartenlänge ist okay, muss mindestens 3 sein)
# (Faktor ist die Anzahl, wie oft gesmoothet werden soll)
def smooth_karte(karte, faktor, partsize):
    karte = list(karte)  # TODO: kann nachher wieder weg
    # zusätzliche Seiten anhängen
    karte.insert(0, karte[0].copy())
    karte.append(karte[-1].copy())
    for c in range(len(karte)):
        karte[c].insert(0, karte[c][0])
        karte[c].append(karte[c][-1])
    buffer = karte.copy()

    # enthält einzelne Zeilen die von den Prozessen übernommen werden
    teile = []

    # TODO: bessere Methode, um die Anzahl Abschnitten zu ermitteln
    failed = True  # ist false, wenn es geschafft wurde alles so aufzuteilen, dass jeder Streifen mindestens 3 lang ist
    bereits_geändert = False  # ist True, wenn die partsize bereits extrem klein gestellt wurde
    while failed:
        teile = []
        while len(buffer) > 1:
            zeug = []
            for c in range(partsize):
                if c in range(len(buffer)):
                    zeug.append(buffer[c])

            for c in range(partsize - 2):
                if len(buffer) != 0:
                    buffer.remove(buffer[0])
            teile.append(zeug)

        if len(teile) != 0:
            if len(teile[-1]) > 3:
                failed = False
            elif partsize > 3 and not bereits_geändert:  # kann kleiner nochmal probiert werden, wenn noch nicht komplett runtergestellt worden
                partsize -= 1
            else:
                buffer = karte.copy()
                bereits_geändert = True
                partsize += 1
                if partsize > len(buffer):
                    print('Diese Kartengröße funktioniert leider nicht. Sie beträgt: ' + str(len(buffer)))
                    sys.exit()

    p = Pool()

    func = partial(smooth, h=faktor)
    result = p.map(func, iterable=teile)

    p.close()
    p.join()

    glatt = []
    for c in range(1, len(result)):
        result[c].remove(result[c][0])
    for c in range(len(result) - 1):
        buffer2 = result[c][:-1]
        for d in buffer2:
            glatt.append(d)
    for c in result[-1]:
        glatt.append(c)

    # die zusätzlichen Seiten wieder entfernen
    glatt.remove(glatt[0])
    glatt = glatt[:-1]
    for c in range(len(glatt)):
        glatt[c].remove(glatt[c][0])
        glatt[c] = glatt[c][:-1]

    return glatt


# platziert bei einer angegebenen Position einen kreisrunden Berg, mit der bei maxi angegeben maximalhöhe (wird auf vor-
# handenes Terrain raufaddiert), der radius gibt den Radius von dem Berg an
def place_circle(karte, x, y, maxi, radius):
    bereich = [(x - radius, x + radius), (y - radius, y + radius)]  # der Bereich in dem der Berg gebaut wird

    if bereich[0][0] < 0:
        bereich[0][0] = 0
    if bereich[0][1] >= len(karte[0]):
        bereich[0][1] = len(karte[0]) - 1
    if bereich[1][0] < 0:
        bereich[1][0] = 0
    if bereich[1][1] >= len(karte):
        bereich[1][1] = len(karte) - 1

    for a in range(len(bereich)):  # Y
        for b in range(len(bereich[a])):  # X
            distanz = pythagoras(karte[b][a], karte[y][x])
            if distanz < radius:
                karte[b][a] += maxi ** (1/distanz)

    return karte


# nimmt X/Y Koordinate zweier Punkte und gibt deren Distanz zurück
def pythagoras(a, b):
    return math.sqrt((abs(a[0] - b[0]) ** 2) + (abs(a[1] - b[1]) ** 2))


# glättet einen bestimmten Abschnitt (wird vorher geteilt) von der Karte
def smooth(karte, h):
    buffer = karte.copy()
    for c in range(h):
        karte = buffer.copy()
        for a in range(1, len(buffer) - 1):
            for b in range(1, len(buffer[a]) - 1):
                buffer[a][b] = (karte[a][b] + karte[a - 1][b] + karte[a - 1][b - 1] + karte[a][b - 1] +karte[a + 1][b - 1] + karte[a + 1][b] + karte[a + 1][b + 1] + karte[a][b + 1] + karte[a - 1][b + 1]) / 9
                #buffer[a][b] = '_'
    return buffer


def scale_map(karte):
    maximum = 0
    for q in range(len(karte)):
        for r in range(len(karte)):
            if maximum < karte[q][r]:
                maximum = karte[q][r]

    scale = 255 / maximum
    for q in range(len(karte)):
        for r in range(len(karte)):
            karte[q][r] = int(karte[q][r] * scale)
    return karte


def make_png(karte, file, size):
    img = Image.new('RGB', (size, size))
    img.putdata(karte)
    img.save(file)


def zeichne_feld(a):
    l = len(a) ** 2 + 1
    for i in a:
        print_string = ""
        for j in i:
            print_string += ((len(str(l)) + 1 - len(str(j))) * " ") + str(j)
        print(print_string)
    print("")


if __name__ == '__main__':
    Größe = 10000
    Karte = [[random.randrange(0, 10) for i in range(Größe)] for j in range(Größe)]

    print('Karte wurde erstellt')

    Karte = scale_map(Karte)

    Fertig = []
    for c in Karte:
        for d in c:
            e = int(d)
            Fertig.append((e, e, e))
    make_png(Fertig, 'Test1.png', len(Karte))

    for i in range(1):
        Karte = smooth_karte(Karte, 1, 3)

    Fertig = []
    for c in Karte:
        for d in c:
            e = int(d)
            Fertig.append((e, e, e))
    make_png(Fertig, 'Test2.png', len(Karte))
