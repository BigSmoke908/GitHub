import random
from PIL import Image
import time
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp

LayerBereich = [2, 12]  # gibt den Bereich an, in dem sich der Faktor von den Layern während dem erstellen befindet, ist minimal 1 und maximal die 2er Potenz, mit der man auf die Größe der Map kommt (je größer, desto glatteres Terrain)
mapSize = 2048  # Größe der Map in Höhe mal Breite (muss eine 2er Potenz sein)
Map = []  # soll als List (alle Zeilen einfach hintereinander die Karte sein
begin = time.time()


# generiert eine Heightmap, indem verschiedene Layer übereinander gelegt werden, min/max sind mindest/maximal Höhe
def generate_heightmap(layerbereich, size):
    height_map = [[0 for i in range(size)] for j in range(size)]
    layermaps = {}  # speichert die Karte von jedem einzelnen

    # es sollen nacheinander verschiedene Bereiche erstelle werden, welche dann eine Höhe erhalten, welche dann alle
    # zusammen diesen Layer bilden sollen
    h = layerbereich[0]
    while h <= layerbereich[1]:
        bereiche = []  # immer die Begrenzungen von einem Bereich

        #  die Maße von den momentanen Bereichen

        length = size
        for i in range(h):
            length /= 2

        # generiert für jedes einzelne Layer die Bereiche, diese erhalten noch keine Höhe (wird erst bei dem nächsten Schritt festgelegt
        for i in range(1, size + 1):  # Loop für alle Werte (da immer ein Quadrat entsteht, reicht eine Seitenkante
            if i % length == 0 and i not in bereiche:
                bereiche.append(i)

        layermaps.update({h: []})
        layermaps[h] = bereiche     # enthält dann von allen Layern den Bereich (wo die Höhe jeweils wirkt) und
                                    # den Betrag (von der jeweiligen Höhe)
        h += 1

    print('Einzelne Schichten wurden erstellt. Die Schichten werden jetzt zusammengefügt')

    for i in layermaps:  # alle einzelnen Karten durchgehen (i entspricht h von vorher)
        tile_y = 0  # Y Platz (in der List) von dem Tile, welches gerade genutzt wird
        tile_x = 0  # X Platz (in der List) von dem Tile, welches gerade genutzt wird
        y = 0  # Y Koordinate auf der heightmap
        x = 0  # X Koordinate auf der heightmap

        momentane_karte = layermaps[i]  # (ist dann einfacher bei jedes Mal aufrufen)

        momentane_höhen = [[random.randrange(0, 255) for j in range(len(momentane_karte))] for k in range(len(momentane_karte))]
        # eine Karte in der die Höhen der einzelnen Tiles drinstehen

        while True:  # fügt alle einzelnen Karten zusammen
            if y == len(height_map):  # am Boden angekommen?
                break
            elif x == len(height_map):  # an der rechten Wand angekommen
                x = 0
                tile_x = 0
                y += 1
            elif y == momentane_karte[tile_y]:  # muss das Tile geändert werden?
                tile_y += 1
            elif x == momentane_karte[tile_x]:  # muss das Tile geändert werden?
                tile_x += 1
            else:  # die Höhe kann bei dem jeweiligen eingetragen werden
                height_map[y][x] = (height_map[y][x] * 2) + momentane_höhen[tile_y][tile_x]
                x += 1

        print('Es wurde eine neue Schicht hinzugefügt und die Karte wird gerade geglättet. Das ist Schicht Nummer ' + str(i))
        height_map = mp_smooth_map(height_map, i)

    print('Die Schichten wurden zusammengefügt. Jetzt werden die Daten "bereinigt"')

    # jetzt müssen die Datenpunkte noch so erhöht/erniedrigt werden, dass sie zwischen 0 und 255 liegen
    height_map = scale_map(height_map)

    print('Die Heightmap wurde fertig erstellt, jetzt wird sie in eine Bilddatei umgewandelt')
    return height_map


# generiert eine Heightmap, indem verschiedene Layer übereinander gelegt werden, min/max sind mindest/maximal Höhe
def generate_heightmap(layerbereich, size):
    height_map = [[0 for i in range(size)] for j in range(size)]
    layermaps = {}  # speichert die Karte von jedem einzelnen

    # es sollen nacheinander verschiedene Bereiche erstelle werden, welche dann eine Höhe erhalten, welche dann alle
    # zusammen diesen Layer bilden sollen
    h = layerbereich[0]
    while h <= layerbereich[1]:
        bereiche = []  # immer die Begrenzungen von einem Bereich

        #  die Maße von den momentanen Bereichen

        length = size
        for i in range(h):
            length /= 2

        # generiert für jedes einzelne Layer die Bereiche, diese erhalten noch keine Höhe (wird erst bei dem nächsten Schritt festgelegt
        for i in range(1, size + 1):  # Loop für alle Werte (da immer ein Quadrat entsteht, reicht eine Seitenkante
            if i % length == 0 and i not in bereiche:
                bereiche.append(i)

        layermaps.update({h: []})
        layermaps[h] = bereiche     # enthält dann von allen Layern den Bereich (wo die Höhe jeweils wirkt) und
                                    # den Betrag (von der jeweiligen Höhe)
        h += 1

    print('Einzelne Schichten wurden erstellt. Die Schichten werden jetzt zusammengefügt')

    for i in layermaps:  # alle einzelnen Karten durchgehen (i entspricht h von vorher)
        tile_y = 0  # Y Platz (in der List) von dem Tile, welches gerade genutzt wird
        tile_x = 0  # X Platz (in der List) von dem Tile, welches gerade genutzt wird
        y = 0  # Y Koordinate auf der heightmap
        x = 0  # X Koordinate auf der heightmap

        momentane_karte = layermaps[i]  # (ist dann einfacher bei jedes Mal aufrufen)

        momentane_höhen = [[random.randrange(0, 255) for j in range(len(momentane_karte))] for k in range(len(momentane_karte))]
        # eine Karte in der die Höhen der einzelnen Tiles drinstehen

        while True:  # fügt alle einzelnen Karten zusammen
            if y == len(height_map):  # am Boden angekommen?
                break
            elif x == len(height_map):  # an der rechten Wand angekommen
                x = 0
                tile_x = 0
                y += 1
            elif y == momentane_karte[tile_y]:  # muss das Tile geändert werden?
                tile_y += 1
            elif x == momentane_karte[tile_x]:  # muss das Tile geändert werden?
                tile_x += 1
            else:  # die Höhe kann bei dem jeweiligen eingetragen werden
                height_map[y][x] = (height_map[y][x] * 2) + momentane_höhen[tile_y][tile_x]
                x += 1

        print('Es wurde eine neue Schicht hinzugefügt und die Karte wird gerade geglättet. Das ist Schicht Nummer ' + str(i))
        height_map = smooth_map(height_map, i)

    print('Die Schichten wurden zusammengefügt. Jetzt werden die Daten "bereinigt"')

    # jetzt müssen die Datenpunkte noch so erhöht/erniedrigt werden, dass sie zwischen 0 und 255 liegen
    height_map = scale_map(height_map)

    print('Die Heightmap wurde fertig erstellt, jetzt wird sie in eine Bilddatei umgewandelt')
    return height_map


# generiert eine Heightmap, indem verschiedene Layer übereinander gelegt werden, min/max sind mindest/maximal Höhe
def generate_andere_heightmap(layerbereich, size):
    height_map = [[-1 for i in range(size)] for j in range(size)]
    layermaps = {}  # speichert die Karte von jedem einzelnen

    # es sollen nacheinander verschiedene Bereiche erstelle werden, welche dann eine Höhe erhalten, welche dann alle
    # zusammen diesen Layer bilden sollen
    h = layerbereich[0]
    while h <= layerbereich[1]:
        bereiche = []  # immer die Begrenzungen von einem Bereich

        #  die Maße von den momentanen Bereichen

        length = size
        for i in range(h):
            length /= 2

        # generiert für jedes einzelne Layer die Bereiche, diese erhalten noch keine Höhe (wird erst bei dem nächsten Schritt festgelegt
        for i in range(1, size + 1):  # Loop für alle Werte (da immer ein Quadrat entsteht, reicht eine Seitenkante
            if i % length == 0 and i not in bereiche:
                bereiche.append(i)

        layermaps.update({h: []})
        layermaps[h] = bereiche     # enthält dann von allen Layern den Bereich (wo die Höhe jeweils wirkt) und
                                    # den Betrag (von der jeweiligen Höhe)
        h += 1

    print('Einzelne Schichten wurden erstellt. Die Schichten werden jetzt zusammengefügt')

    for i in layermaps:  # alle einzelnen Karten durchgehen (i entspricht h von vorher)
        tile_y = 0  # Y Platz (in der List) von dem Tile, welches gerade genutzt wird
        tile_x = 0  # X Platz (in der List) von dem Tile, welches gerade genutzt wird
        y = 0  # Y Koordinate auf der heightmap
        x = 0  # X Koordinate auf der heightmap

        momentane_karte = layermaps[i]  # (ist dann einfacher bei jedes Mal aufrufen)

        momentane_höhen =[[-1 for j in range(len(momentane_karte))] for k in range(len(momentane_karte))]
        # eine Karte in der die Höhen der einzelnen Tiles drinstehen

        while True:  # fügt alle einzelnen Karten zusammen
            if y == len(height_map):  # am Boden angekommen?
                break
            elif x == len(height_map):  # an der rechten Wand angekommen
                x = 0
                tile_x = 0
                y += 1
            elif y == momentane_karte[tile_y]:  # muss das Tile geändert werden?
                tile_y += 1
            elif x == momentane_karte[tile_x]:  # muss das Tile geändert werden?
                tile_x += 1
            else:  # die Höhe kann bei dem jeweiligen eingetragen werden
                if momentane_höhen[tile_y][tile_x] == -1 and height_map[x][y] != -1:
                    momentane_höhen[tile_y][tile_x] = random.randrange(height_map[x][y] - 10, height_map[x][y] + 10)
                elif momentane_höhen [tile_y][tile_x] == -1 and height_map[x][y] == -1:
                    momentane_höhen[tile_y][tile_x] = random.randrange(0, 255)
                height_map[y][x] = momentane_höhen[tile_y][tile_x]
                x += 1

        print('Es wurde eine neue Schicht hinzugefügt und die Karte wird gerade geglättet. Das ist Schicht Nummer ' + str(i))

        # die momentane Karte in ein Bild umwandeln
        buffer = []
        maximum = 0
        for k in range(len(height_map)):
            for l in range(len(height_map)):
                höhe = height_map[k][l]
                buffer.append(höhe)
                if höhe > maximum:
                    maximum = höhe

        scale = 255 / maximum
        for nummer in range(len(buffer)):
            höhe = int(buffer[nummer] * scale)
            buffer[nummer] = (höhe, höhe, höhe)
        make_png(buffer, 'Heightmap_test/' + str(i) + '.png', size)

    render_heightmap(height_map)

    height_map = smooth_map(height_map, 1)

    print('Die Schichten wurden zusammengefügt. Jetzt werden die Daten "bereinigt"')

    # jetzt müssen die Datenpunkte noch so erhöht/erniedrigt werden, dass sie zwischen 0 und 255 liegen
    height_map = scale_map(height_map)

    print('Die Heightmap wurde fertig erstellt, jetzt wird sie in eine Bilddatei umgewandelt')
    return height_map


# nimmt ein Heightmap und glättet sie etwas (Punkte die nebeneinander liegen, bekommen eine ähnliche Höhe)
# macht mitunter seltsame Dinge, könnte vielleicht noch verbessert werden (Durchschnitt von mehr als nur 9 Feldern bespielsweise)
def smooth_map(karte, h):
    buffer = karte.copy()
    for c in range(100//h):
        karte = buffer.copy()
        for a in range(1, len(karte) - 1):
            for b in range(1, len(karte) - 1):
                buffer[a][b] = (karte[a][b] + karte[a - 1][b] + karte[a - 1][b - 1] + karte[a][b - 1] + karte[a + 1][b - 1] + karte[a + 1][b] + karte[a + 1][b + 1] + karte[a][b + 1] + karte[a - 1][b + 1]) // 9
    return buffer


# ist das smoothen für das Multiprocessing + an jeden Kartensektor wird hinten angehängt welcher Sektor das ist
def smooth_map_neu(karte, h, q, sector):
    karte = smooth_map(karte, h)
    karte.append(sector)
    q.put(karte)


# macht das gleich wie das andere smoothen, aber hoffentlich deutlich schneller (teilt das smoothen in 4 Einzelprozesse)
# die Funktion ruft auch letztendlich nur wieder die anderen smoothing Karte mit mehreren Unterprozessen auf
def mp_smooth_map(karte, h):
    # als erstes die Karte in 4 einzelne Prozesse unterteilen, welche dann normal geglättet werden
    maße = [(len(karte)//2) + 1, (len(karte)//2) - 1, len(karte)]  # speichert die einzelnen Parameter (müssen nicht zig mal aufgerufen werden)
    buffer1 = [[karte[y][x] for x in range(0, maße[0])] for y in range(0, maße[0])]  # oben Links
    buffer2 = [[karte[y][x] for x in range(maße[1], maße[2])] for y in range(0, maße[0])]  # oben Rechts
    buffer3 = [[karte[y][x] for x in range(0, maße[0])] for y in range(maße[1], maße[2])]  # unten Links
    buffer4 = [[karte[y][x] for x in range(maße[1], maße[2])] for y in range(maße[1], maße[2])]  # unten Rechts

    if __name__ == '__main__':
        q = mp.Queue()
        # erstelle mit den einzelnen Karten die Prozesse
        p1 = mp.Process(target=smooth_map_neu, args=(buffer1, h, q, 1))
        p2 = mp.Process(target=smooth_map_neu, args=(buffer2, h, q, 2))
        p3 = mp.Process(target=smooth_map_neu, args=(buffer3, h, q, 3))
        p4 = mp.Process(target=smooth_map_neu, args=(buffer4, h, q, 4))

        prozesse = [p1, p2, p3, p4]
        # alle Prozesse werden gestartet
        for p in prozesse:
            p.start()

        ergebnisse = [q.get() for p in prozesse]  # enthält alle 4 Sektoren, aber wohlmöglich in falscher Reihenfolge!!

        del q
        # alle Prozesse werden beendet
        for p in prozesse:
            p.join()

        print('Das eigentlich smoothen ist abgeschlossen, jetzt werden die Daten wieder zusammengefügt')

        sektoren = []  # soll alle einzelnen Sektoren in richtiger Reihenfolge speichern (wird hiernach gemacht)
        while len(sektoren) < len(ergebnisse):
            for i in ergebnisse:
                if i[-1] - 1 == len(sektoren):  # wenn das der Sektor ist, der angefügt werden muss
                    sektoren.append(i)

        # jetzt werden von den einzelnen Sektoren wieder die Teile abgenommen, die doppelt ist
        for i in sektoren:
            copy = i.copy()
            if i[-1] == 1:  # erster Sektor
                copy = copy[:-1]  # das Kennzeichen von i
                copy = copy[:-1]  # unnötige X
                for j in range(len(copy)):
                    copy[j] = copy[j][:-1]  # unnötige Y
            elif i[-1] == 2:  # zweiter Sektor
                copy = copy[:-1]  # das Kennzeichen von i
                copy = copy[:-1]  # unnötige Y
                for j in range(len(copy)):
                    del copy[j][0]  # unnötige X
            elif i[-1] == 3:  # dritter Sektor
                copy = copy[:-1]  # das Kennzeichen von i
                del copy[0]  # unnötige Y
                for j in range(len(copy)):
                    copy[j] = copy[j][:-1]  # unnötige X
            elif i[-1] == 4:  # vierter Sektor
                copy = copy[:-1]  # das Kennzeichen von i
                del copy[0]  # unnötige Y
                for j in range(len(copy)):  # unnötige X
                    del copy[j][0]
            sektoren[sektoren.index(i)] = copy  # wieder in alle Sektoren zurücktun

        glatte_karte = [[0 for i in range(len(karte))] for j in range(len(karte))]  # soll die fertige Karte werden
        for i in range(len(sektoren)):
            sektor = sektoren[i]
            offset_x = 0  # wie viel zu X/Y addiert werden muss in den jeweiligen Sektoren
            offset_y = 0
            seitenlänge = len(karte) // 2  # -> muss nur einmal berechnet werden

            if i == 1:  # 2. Sektor, bei dem ersten gibt es kein Offset (deshalb weggelassen)
                offset_x = seitenlänge
            elif i == 2:  # 3. Sektor
                offset_y = seitenlänge
            elif i == 3:  # 4. Sektor
                offset_x = seitenlänge
                offset_y = seitenlänge

            for a in range(seitenlänge):
                for b in range(seitenlänge):
                    glatte_karte[a + offset_y][b + offset_x] = sektor[a][b]
    return glatte_karte


def make_png(map, file, size):
    img = Image.new('RGB', (size, size))
    img.putdata(map)
    img.save(file)


def scale_map(map):
    maximum = 0
    for q in range(len(map)):
        for r in range(len(map)):
            if maximum < map[q][r]:
                maximum = map[q][r]

    scale = 255 / maximum
    for q in range(len(map)):
        for r in range(len(map)):
            map[q][r] = int(map[q][r] * scale)
    return map


def erosion(iterationen, karte):
    for tropfen in range(iterationen):
        # TODO: einen Wassertropfen simulieren, der die Map entlangfließt und Sedimente mitnimmt/abgibt etc.
        x, y = random.randrange(1, len(karte) - 1), random.randrange(1, len(karte) - 1)
        momentum = 0  # wie viel Schwung das Teilchen gerade hat (1 bedeutet es kann 1 hochfließen)
        height = karte[y][x]
        sedimente = 0  # wie viele Sedimente der Tropfen gerade mit sich trägt (bei Beschleunigen wird abgetragen, bei verlangsamen wird abgelagert)
        richtung = 0  # geht von 0 bis 8, gibt an in welche Richtung der Tropfen gerade fließt (0 ist nach rechts, dann im Uhrzeigersinn alle Felder neben dem Tropfen)
        bewegung = 4  # wird verringert wenn keine Bewegung ist, und auf 4 gesetzt wenn Bewegung vorhanden ist

        while bewegung != 0 or momentum != 0:
            feld = (256, 0, 0)  # speichert die Höhe, die X- und die Y Koordinate von dem niedrigsten Feld in der Umgebung

            feld_in_richtung = ()

            for zeug in range(3):
                if karte[y - 1][(x - 1) + zeug] < feld[0]:  # für die oberen 3 Felder
                    feld = (karte[y - 1][(x - 1) + zeug], y - 1, (x - 1) + zeug)
                if karte[y][(x - 1) + zeug] < feld[0]:  # für die mittleren 3 Felder
                    feld = (karte[y][(x - 1) + zeug], y, (x - 1) + zeug)
                if karte[y + 1][(x - 1) + zeug] < feld[0]:  # die unteren 3 Felder
                    feld = (karte[y + 1][(x - 1) + zeug], y + 1, (x - 1) + zeug)
    return karte


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
    Map = generate_heightmap(LayerBereich, mapSize)

    Fertig = []
    for i in range(len(Map)):
        for j in range(len(Map)):
            Fertig.append((Map[i][j], Map[i][j], Map[i][j]))

    make_png(Fertig, 'Heightmap_test/Fertig.png', mapSize)

    print('alles ist abgeschlossen')

    print('Die Heightmap wird jetzt angezeigt')

    end = time.time() - begin
    print('Das Rendern hat ' + str(end) + ' Sekunden gedauert')
    render_heightmap(Map)
