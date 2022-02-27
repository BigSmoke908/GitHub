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
    # TODO: momentan wird einfach nur so oft wie der Faktor sagt jeder Abschnitt alleine gesmoothet, aber nicht zusammen

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


# TODO: maximum noch integrieren
# platziert bei einer angegebenen Position einen kreisrunden Berg, mit der bei maxi angegeben maximalhöhe (wird auf vor-
# handenes Terrain raufaddiert), der radius gibt den Radius von dem Berg an
def place_circle(karte, pos, maxi, radius):
    bereich = [[pos[0] - radius, pos[0] + radius], [pos[1] - radius, pos[1] + radius]]  # der Bereich in dem der Berg gebaut wird

    if bereich[0][0] < 0:
        bereich[0][0] = 0
    if bereich[0][1] >= len(karte[0]):
        bereich[0][1] = len(karte[0])
    if bereich[1][0] < 0:
        bereich[1][0] = 0
    if bereich[1][1] >= len(karte):
        bereich[1][1] = len(karte)

    offset = -1  # wie viel alles erhöht werden muss (damit keine negativen Werte entstehen)
    for a in range(bereich[0][0], bereich[0][1]):  # Y
        for b in range(bereich[1][0], bereich[1][1]):  # X
            distanz = pythagoras((b, a), pos)
            if distanz < radius:
                if offset == -1:  # wir sind an einem Punkt, der am weitesten weg ist
                    mitte = [(int(abs(bereich[0][0] - bereich[0][1]))), (int(abs(bereich[1][0] - bereich[1][1])))]
                    buffer_distanz = pythagoras(mitte, pos)
                    offset = abs((-2 * buffer_distanz) - (buffer_distanz ** 2))
                    height = ((-2 * distanz) - (distanz ** 2) + offset) * radius
                    if height < 0:
                        height = 0
                karte[a][b] += height
    return karte


# nimmt X/Y Koordinate zweier Punkte und gibt deren Distanz zurück
def pythagoras(a, b):
    return math.sqrt((abs(a[0] - b[0]) ** 2) + (abs(a[1] - b[1]) ** 2)) + 1


# glättet einen bestimmten Abschnitt (wird vorher geteilt) von der Karte
def smooth(karte, h):
    buffer = karte.copy()
    for c in range(h):
        karte = buffer.copy()
        for a in range(1, len(buffer) - 1):
            for b in range(1, len(buffer[a]) - 1):
                buffer[a][b] = (karte[a][b] + karte[a - 1][b] + karte[a - 1][b - 1] + karte[a][b - 1] + karte[a + 1][b - 1] + karte[a + 1][b] + karte[a + 1][b + 1] + karte[a][b + 1] + karte[a - 1][b + 1]) / 9
                #buffer[a][b] = '_'
    return buffer


def scale_map(karte):
    alles = [karte[i][j] for i in range(len(karte)) for j in range(len(karte))]
    maximum = max(alles)

    if maximum != 0:
        scale = 255 / maximum
    else:
        scale = 1
    for q in range(len(karte)):
        for r in range(len(karte)):
            karte[q][r] = int(karte[q][r] * scale)
    return karte


def make_png(karte, file):
    karte = scale_map(karte)
    fertig = [(karte[a][b], karte[a][b], karte[a][b]) for a in range(len(karte)) for b in range(len(karte))]
    img = Image.new('RGB', (len(karte), len(karte)))
    img.putdata(fertig)
    img.save(file)
    print('Die Datei "' + file + '" wurde erstellt.')


def zeichne_feld(a):
    l = len(a) ** 2 + 1
    for i in a:
        print_string = ""
        for j in i:
            print_string += ((len(str(l)) + 1 - len(str(j))) * " ") + str(j)
        print(print_string)
    print("")


def render_heightmap(map):
    z = np.array([[map[y][x] for x in range(len(map))] for y in range(len(map))])
    x, y = np.meshgrid(range(z.shape[0]), range(z.shape[1]))

    # show hight map in 3d
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z)
    plt.title('z as 3d height map')
    plt.show()


if __name__ == '__main__':
    X = 4096
    Y = 4096
    Karte = [[0 for i in range(X)] for j in range(Y)]

    print('Karte wurde erstellt')

    make_png(Karte, 'Test1.png')

    print('Der Berg wird platziert')
    for i in range(1):
        Pos = (random.randrange(0, X), random.randrange(0, Y))
        Radius = random.randrange(1000, 1100)
        Karte = place_circle(Karte, Pos, 10, Radius)
        print(Pos, Radius)

    make_png(Karte, 'Test2.png')

    for i in range(10):
        Karte = smooth_karte(Karte, 1, 400)

    make_png(Karte, 'Test3.png')

    render_heightmap(Karte)
