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
            buffer3 = [int(buffer[i])]
            buffer2 = i % 4
            if buffer2 != 3:
                daten[buffer2].append(buffer[i])
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
                cluster[i][j] = random.randrange(0, 10, 1)

        distanzen = {
            0:[],
            1:[],
            2:[]
        }
        # darin sollen die Distanzen von Punkten zu einzelnen Clustern gespeichert werden (Key entspricht Cluster)

        changes = True

        while changes:
            changes = False

            for i in range(len(daten)):
                for j in range(len(cluster)):
                    if i > len(distanzen[0]):
                        # TODO: die Distanzen berechnen
                        pass
                    else:
                        # TODO: die Distanzen berechnen
                        pass



k_means()