import time
import heightmap
import multiprocessing as mp
import random

seite = 4096
map = [[random.randrange(0, 10) for i in range(seite)] for j in range(seite)]


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
        p1 = mp.Process(target=heightmap.smooth_map_neu, args=(buffer1, h, q, 1))
        p2 = mp.Process(target=heightmap.smooth_map_neu, args=(buffer2, h, q, 2))
        p3 = mp.Process(target=heightmap.smooth_map_neu, args=(buffer3, h, q, 3))
        p4 = mp.Process(target=heightmap.smooth_map_neu, args=(buffer4, h, q, 4))

        prozesse = [p1, p2, p3, p4]
        # alle Prozesse werden gestartet
        for p in prozesse:
            p.start()

        ergebnisse = [q.get() for p in prozesse]  # enthält alle 4 Sektoren, aber wohlmöglich in falscher Reihenfolge!!

        del q
        # alle Prozesse werden beendet
        for p in prozesse:
            p.join()

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


if __name__ == '__main__':
    begin = time.time()
    mp_smooth_map(map, 1)
    print(str(time.time() - begin) + ' MP\n\n')

    begin = time.time()
    heightmap.smooth_map(map, 1)
    print(str(time.time() - begin) + ' SP\n\n')
