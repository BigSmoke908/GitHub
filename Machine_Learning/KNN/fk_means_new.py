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
        print(buffer, '\n')
        while len(buffer) != 0:
            buffer.remove(buffer[0])
        anfang, changes = True, True

        iterationen = 0
        while changes:
            if (iterationen//100)*100 == iterationen:
                print(cluster)

            changes = False
            buffer = cluster
            for i in range(len(daten[0])):  # Counter für alle Punkte
                a = d(cluster[0][0], daten[0][i]) + d(cluster[0][1], daten[1][i]) + d(cluster[0][2], daten[2][i])
                b = d(cluster[1][0], daten[0][i]) + d(cluster[1][1], daten[1][i]) + d(cluster[1][2], daten[2][i])
                c = d(cluster[2][0], daten[0][i]) + d(cluster[2][1], daten[1][i]) + d(cluster[2][2], daten[2][i])
                # Abstand zu allen einzelnen buffern
                # es wird sortiert, zu welchem buffer der Abstand am kleinsten ist
                if a < b:
                    if a < c:
                        # a ist am kleinsten
                        for j in range(len(buffer[0]) - 1):
                            buffer[0][j] += daten[j][i]
                        buffer[0][len(buffer[0]) - 1] += 1
                    else:
                        # c ist am kleinsten
                        buffer[2][j] += daten[j][i]
                        buffer[2][len(buffer[0]) - 1] += 1
                else:
                    if b < c:
                        # b ist am kleinsten
                        buffer[1][j] += daten[j][i]
                        buffer[1][len(buffer[0]) - 1] += 1
                    else:
                        # c ist am kleinsten
                        buffer[2][j] += daten[j][i]
                        buffer[2][len(buffer[0]) - 1] += 1

            for i in range(len(buffer)):  # Counter für alle neuen Cluster
                for j in range(len(buffer[i]) - 1):  # Counter für alle Parameter des neuen Clusters
                    if buffer[i][len(buffer[i]) - 1] != 0:
                        buffer[i][j] = buffer[i][j] / buffer[i][len(buffer[i]) - 1]

            if cluster != buffer:
                changes = True
                cluster = buffer
            iterationen += 1
    return


k_means()
print(cluster)