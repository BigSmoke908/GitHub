import random
import sys
import pygame
import math
from functools import partial


screen = pygame.display.set_mode((2560, 1440))
pygame.init()

# enthält x/y Koordinaten von allen Ameisen + Drehung der Ameise (0 = rechts) + ob die Ameise gerade Essen trägt oder nicht
# [x, y, Winkel, False]  (True, wenn die Ameise gerade Essen trägt)
Ameisen = [[random.randrange(100, 2460), random.randrange(100, 1340), random.randrange(0, 360), bool(random.randrange(0, 2))] for i in range(1)]
Pheromone = []  # enthält Punkte an den Pheromone sind + die Konzentration von diesen: [x, y, konzentration]


def kopf(winkel, d, x, y):
    return [d * math.cos(math.radians(winkel)) + x, d * math.sin(math.radians(winkel)) + y]


# nimmt eine Ameise und überprüft, ob in dem vorderen Sichtfeld Pheromone sind
def check_view(ameise):
    # felder_dicht = [[kopf(ameise[2], 0.5)]]
    return


def check(gesucht, element):
    if [element[0], element[1]] == gesucht:
        return True
    return False


# sucht in der List (heuhaufen), nach einer List, weclche in den ersten beiden Element mit der Nadel übereinstimmt
# gibt den Index davon zurück, wenn die nadel vorhanden ist, sonst wird None zurückgegeben
def suchen(heuhaufen, nadel):
    func = partial(check, gesucht=nadel)
    gefunden = list(filter(func, heuhaufen))
    print(gefunden)


def render(ant_size=1.0):
    screen.fill((120, 110, 110))
    for ameise in Ameisen:
        if ameise[3]:
            pygame.draw.circle(screen, (90, 70, 0), (ameise[0], ameise[1]), int(10 * ant_size))
            pygame.draw.circle(screen, (90, 70, 0), (kopf(ameise[2], int(14 * ant_size), ameise[0], ameise[1])), int(6 * ant_size))
        else:
            pygame.draw.circle(screen, (0, 0, 0), (ameise[0], ameise[1]), int(10 * ant_size))
            pygame.draw.circle(screen, (0, 0, 0), (kopf(ameise[2], int(14 * ant_size), ameise[0], ameise[1])), int(6 * ant_size))
    render_pheromone()
    pygame.display.update()


def render_pheromone():
    for punkt in Pheromone:
        if punkt[2] <= 5.1:
            pygame.draw.rect(screen, (0, punkt[2] * 20, 0), (punkt[0], punkt[1], 1, 1))
        else:
            pygame.draw.rect(screen, (0, 255, 0), (punkt[0], punkt[1], 1, 1))


def walk():
    global Ameisen

    for ameise in Ameisen:
        ameise[2] += random.randrange(-5, 6)
        neu = kopf(ameise[2], 0.5, ameise[0], ameise[1])
        while neu[0] < 10 or neu[0] > 2540 or neu[1] < 0 or neu[1] > 1430:
            ameise[2] += random.randrange(-100, 100)
            neu = kopf(ameise[2], 0.5, ameise[0], ameise[1])
        ameise[0], ameise[1] = neu[0], neu[1]
        ameise[2] %= 360


while False:
    render(0.5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    walk()

suchen([[42, 23, 12], [69, 17, 13], [18, 21, 9]], [42, 23])
