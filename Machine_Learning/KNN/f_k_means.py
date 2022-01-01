import random
from func_fuer_ml import distanz as d

def k_means():
    with open('bekannt.txt') as f:
        global daten, cluster
        daten = {0: [], 1: [], 2: []}
        buffer = f.read()
        buffer = buffer.split()

        for i in range(len(buffer)):
            buffer2 = i % 4
            if buffer2 != 3:
                daten[buffer2].append(int(buffer[i]))
        # in Daten sind die drei Koordinaten von Punkten

        # hier werden die Koordinaten der einzelnen Cluster gespeichert
        # der hinterste Wert gibt (erst später) die Anzahl der Punkte die dem Cluster angehören an
        cluster = {0: [0, 0, 0, 0], 1: [0, 0, 0, 0], 2: [0, 0, 0, 0]}
        # hier wird jedem Cluster eine Position gegeben
        for i in range(len(cluster)):
            for j in range(len(cluster[0]) - 1):
                cluster[i][j] = random.randrange(0, 100, 1)
        distanzen = {0: [], 1: [], 2: [], 3: []}
        # darin sollen die Distanzen von Punkten zu einzelnen Clustern gespeichert werden (Key entspricht Cluster)
        # letzter Key ist aber aber immer einfach eine Liste mit dem dichtesten Cluster (Reihenfolge so wie in Daten)
        while len(buffer) != 0:
            buffer.remove(buffer[0])
        anfang, changes = True, True

        iterationen = 0
        while changes:
            changes = False

            if (iterationen//100)*100 == iterationen:
                print('momentane Cluster ' + str(cluster))
                iterationen = 0
            iterationen += 1

            for i in range(len(daten[0])):
                for j in range(3):
                    if (i - 1) < len(distanzen[j]) and anfang:
                        distanzen[j].append(d(daten[0][i], cluster[0][j]) + d(daten[1][i], cluster[1][j]) + d(daten[2][i], cluster[2][j]))
                    else:
                        distanzen[j][i] = d(daten[0][i], cluster[0][j]) + d(daten[1][i], cluster[1][j]) + d(daten[2][i], cluster[2][j])

            buffer = 0
            # jeder Punkt bekommt in distanzen ein Cluster zugewiesen, zu dem der Abstand am kleinsten ist
            for i in range(len(distanzen[0])):
                for j in range(len(distanzen) - 1):
                    if j == 0:
                        buffer = j
                    elif distanzen[buffer][i] > distanzen[j][i]:
                        buffer = j
                buffer2 = len(distanzen) - 1
                # die Nummer von dem dichtesten Cluster wird gespeichert (selbe Reihenfolge wie vorher)
                if buffer2 < 0:
                    buffer2 = 0
                if i > len(distanzen[buffer2]) and not anfang:
                    distanzen[buffer2][i] = buffer
                else:
                    distanzen[buffer2].append(buffer)

            coord = {0: [0, 0, 0], 1: [0, 0, 0], 2: [0, 0, 0]}
            # dieses Dic speichert vorerst die neuen Koordinaten der Cluster (Key = Cluster, dahinter Koordinaten)
            # hier wird die durchschnittliche Position von Punkten der einem Cluster angehört berechnet
            for i in range(len(distanzen[0])): # Counter für alle Punkte
                cluster[distanzen[len(distanzen) - 1][i]][len(cluster)] += 1 # Counter, der für jedes Clust angibt, wie viele am dichstesten sind

            # jetzt werden die Koordinaten für die Cluster neu berechnet
            for i in range(len(daten[0])): # Counter für alle Punkte
                for j in range(len(coord[0])): # Counter für alle Dimensionen
                    coord[distanzen[len(distanzen) - 1][i]][j] += daten[j][i]

            buffer = [0, 0, 0] # soll für jedes Cluster die Anzahl der dazugehörigen Punkte speichern
            for i in range(len(distanzen[len(distanzen) - 1])): # Counter für alle Punkte
                buffer[distanzen[(len(distanzen) - 1)][i]] += 1

            for i in range(len(coord)): # Counter für alle Cluster
                for j in range(len(coord[i])): # Counter für alle Koordinaten
                    if buffer[i] != 0:
                        coord[i][j] = coord[i][j]/buffer[i]
                        changes = True
                    else:
                        coord[i][j] = cluster[i][j]
                    # in coord befinden sich jetzt die neuen Koordinaten von den Clustern
            for i in range(len(coord)): # Counter für alle Cluster
                for j in range(len(cluster[0])): # Counter für alle Eigenschaften von Clustern
                    if j != 3:
                        cluster[i][j] = coord[i][j]
                    else:
                        cluster[i][3] = 0


k_means()
print(cluster)