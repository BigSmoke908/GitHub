import random
from func_fuer_ml import distanz as d

def k_means():
    with open('bekannt.txt') as f:
        global daten
        daten = {
            0:[],
            1:[],
            2:[],
            3:[]
        }
        buffer = f.read()
        buffer = buffer.split()

        for i in range(len(buffer)):
            buffer2 = i % 4
            if buffer2 != 3:
                daten[buffer2].append(int(buffer[i]))
        # in Daten sind die drei Koordinaten von Punkten und der Key (in dem Dic) zum dichtesten Clusterzentrum
        # hier werden die Koordinaten der einzelnen Cluster gespeichert
        cluster = {
            0:[0, 0, 0],
            1:[0, 0, 0],
            2:[0, 0, 0]
        }
        # hier wird jedem Cluster eine Position gegeben
        for i in range(len(cluster)):
            for j in range(len(cluster[0])):
                cluster[i][j] = random.randrange(0, 100, 1)
        distanzen = {
            0:[],
            1:[],
            2:[],
            3:[]
        }
        # darin sollen die Distanzen von Punkten zu einzelnen Clustern gespeichert werden (Key entspricht Cluster)
        # letzter Key ist aber aber immer einfach eine Liste mit dem dichtesten Cluster
        while len(buffer) != 0:
            buffer.remove(buffer[0])
        anfang, changes = True, True

        while changes:
            changes = False
            print('hier sind die Cluster ' + str(cluster))
            for i in range(len(daten[0])):
                for j in range(3):
                    if (i - 1) < len(distanzen[j]) and anfang:
                        distanzen[j].append(d(daten[0][i], cluster[0][j]) + d(daten[1][i], cluster[1][j]) + d(daten[2][i], cluster[2][j]))
                    else:
                        distanzen[j][i] = d(daten[0][i], cluster[0][j]) + d(daten[1][i], cluster[1][j]) + d(daten[2][i], cluster[2][j])

            buffer = 0
            for i in range(len(distanzen[0])):
                for j in range(len(distanzen) - 1):
                    if i == 0:
                        buffer = j
                    elif buffer > distanzen[j][i]:
                        buffer = j
                buffer2 = len(distanzen) - 1
                if buffer2 < 0:
                    buffer2 = 0
                if i > len(distanzen[buffer2]) and not anfang:
                    distanzen[buffer2][i] = buffer
                else:
                    distanzen[buffer2].append(buffer)

        print(distanzen)



k_means()