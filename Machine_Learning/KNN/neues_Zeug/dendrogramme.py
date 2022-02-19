from main import create_data
import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1920, 1080))


Punkte = [['P', 100, 300, -1], ['P', 700, 300, -1], ['P', 70, 20, -1], ['C', 0, 1, 0], ['C', 2, 3, 1]]
Farben = [(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)) for i in range(len(Punkte))]  # speichert für jeden Punkt/jedes Cluster die Farbe (die Clusterfarben werden jedesmal neu berechnet)
#  enthält Punkte/Cluster
# Format für Punkte:
# Punkte = [[Typ (hier ein 'P', X-Koordinate, Y-Koordinate, -1]]
# Format für Cluster:
# Punkte = [[Type (jetzt ein 'C'), Punkt/Cluster 1, Punkte/Cluster 2, wievieltes Cluster]]
# das wievielte Cluster ist später für das Rendern wichtig (beginnt mit 0, 1, ...)


def render(punktsize):
    screen.fill((0, 0, 0))
    highest_cluster = -1  # speichert bei welchem Cluster die höchste Verschacheltung besteht (die meisten Cluster sind bereits darin vorhanden)
    for a in range(len(Punkte)):
        if Punkte[a][0] == 'C' and Punkte[a][3] >= highest_cluster:
            highest_cluster = Punkte[a][3]

    while highest_cluster != -1:  # einen Kreis um die Punkte herum rendern
        for a in range(len(Punkte)):
            if Punkte[a][0] == 'C' and Punkte[a][3] == highest_cluster:  # alle Punkte die zu dem Cluster dazu gehören mit einem Kreis in der Clusterfarbe drumherum versehen
                in_diesem_cluster = list(im_Cluster(a))

                for b in range(len(in_diesem_cluster)):
                    pygame.draw.circle(screen, get_farbe(a), (Punkte[in_diesem_cluster[b]][1], Punkte[in_diesem_cluster[b]][2]), (punktsize + (5 * highest_cluster)))

        highest_cluster = highest_cluster - 1

    for a in range(len(Punkte)):  # normale Punkte rendern
        if Punkte[a][0] == 'P':
            pygame.draw.circle(screen, Farben[a], (Punkte[a][1], Punkte[a][2]), punktsize)
    pygame.display.update()


# soll für ein Cluster/Punkt die Farbe zurückgeben (beides kann einfach reingetan werden)
def get_farbe(cluster):
    if Punkte[cluster][0] == 'P':  # ES IST EIN PUNKT!!!!!!!!! (so "es ist ein Junge/Mädchen" Stil bei der Geburt)
        return Farben[cluster]
    else:  # ES IST EIN CLUSTER
        farbe = []  # soll hinterher RGB Werte von der Farbe speichern
        buffer1 = Punkte[cluster][1]  # Punkt 1 von dem Cluster
        buffer2 = Punkte[cluster][2]  # Punkt 2 von dem Cluster

        buffer1 = get_farbe(buffer1)  # Farbe von Punkt/Cluster 1
        buffer2 = get_farbe(buffer2)  # Farbe von Punkt/Cluster 2

        for i in range(len(buffer1)):  # durch alle Farbteil loopen
            farbe.append((buffer1[i] + buffer2[i]) / 2)
        return farbe


# gibt eine List aller Punkte die in einem Cluster mit drin sind
def im_Cluster(cluster):
    im_cluster = []
    if Punkte[cluster][0] == 'P':
        return [cluster]

    for x in range(len(Punkte)):
        if x != cluster:
            if x == Punkte[cluster][1]:
                a = im_Cluster(x)  # alle Punkte in Punkt/Cluster 1
                for c in range(len(a)):
                    im_cluster.append(a[c])
            elif x == Punkte[cluster][2]:
                b = im_Cluster(x)
                for c in range(len(b)):
                    im_cluster.append(b[c])
    return im_cluster


# berechnet von einem gegebenen Cluster/Punkt die Position (beides kann einfach reingetan werden)
def get_position(cluster):
    gegeben = (Punkte[cluster][1], Punkte[cluster][2])  # erstellt ein Tupel mit den gebenenen Punkten

    if Punkte[cluster][0] == 'C':  # wenn der Punkt überhaupt ein Cluster ist
        # die Koordinaten von beiden Punkten in extra Koordinaten tun, wenn diese selber Cluster sind -> Funktion erneut aufrufen
        if Punkte[Punkte[cluster][1]][0] == 'C':
            a = get_position(Punkte[cluster][1])
        else:
            buffer = Punkte[cluster][1]  # speichert den Punkt der gerade gegeben ist
            a = [Punkte[buffer][1], Punkte[buffer][2]]
        # Punkt 1 hat jetzt Koordinaten

        if Punkte[Punkte[cluster][2]][0] == 'C':
            b = get_position(Punkte[cluster][2])
        else:
            buffer = Punkte[cluster][2]  # speichert den gerade gegebenen Punkt
            b = [Punkte[buffer][1], Punkte[buffer][2]]
        return [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]

    else:  # wenn das Cluster eigentlich ein Punkt ist
        return [Punkte[cluster][1], Punkte[cluster][2]]


# gibt die Distanz von 2 Punkten/Clustern zurück
def get_distanz(punkt1, punkt2):
    a = get_position(punkt1)[0] - get_position(punkt2)[0]
    b = get_position(punkt1)[1] - get_position(punkt2)[1]

    return math.sqrt(a ** 2 + b ** 2)


while True:
    render(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
