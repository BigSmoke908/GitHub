import math
import pygame
import sys
from multiprocessing import Pool


def prime(x):
    test = 1
    teiler = []
    while test <= math.sqrt(x):
        if x % test == 0:
            if test not in teiler:
                teiler.append(test)
            if x // test not in teiler:
                teiler.append(x // test)
        test += 1

    if len(teiler) == 2:
        return True
    return False


def next_prime(x):
    while True:
        if x % 2 == 0 and x != 0:
            x += 1
        else:
            x += 2
        if prime(x):
            return x


# gibt alle Primzahlen in einem Bereich, hängt hinten noch den Index für das Multiprocessing an
def primzahlen(bereich):
    alle = [next_prime(bereich[0])]

    while alle[-1] < bereich[1]:
        alle.append(next_prime(alle[-1]))

    alle[-1] = bereich[2]
    return alle


# teilt den Bereich auf 11 Unterbereiche auf (mit Runden werden es in seltenen Fällen auch 12 -> Länge Bereich sollte
# immer vielfaches von 11 sein!!)
# gibt außerdem als dritten Wert die Reihenfolge von den Unterbereichen an (später für zusammenfügen ganz hilfreich)
def verteile_bereiche(bereich):
    return [[i, i + (bereich[1] - bereich[0]) // 11, i // ((bereich[1] - bereich[0]) // 11)] for i in range(bereich[0], bereich[1], (bereich[1] - bereich[0]) // 11)]


def calc_primes(bereich):
    primes = []
    aufgaben = verteile_bereiche(bereich)
    p = Pool()
    result = p.map(func=primzahlen, iterable=aufgaben)

    changes = True
    while changes:
        changes = False
        for i in range(1, len(result)):
            if result[i][-1] < result[i - 1][-1]:
                buffer1 = result[i].copy()
                buffer2 = result[i - 1].copy()
                result[i] = buffer2.copy()
                result[i - 1] = buffer1.copy()
                changes = True

    for i in result:
        if len(i) != 0:
            for j in range(len(i) - 1):
                primes.append(i[j])
    return primes


def get_cords(x, zoom=1):
    return [x * math.cos(x) * zoom, x * math.sin(x) * zoom]


if __name__ != '__main__':
    pygame.init()
    screen = pygame.display.set_mode((3840, 2160))
    Primzahlen = []
    # Zoom = 1
    Zoom = 0.0034254873907817516
    Bereich = 0

    background = (0, 0, 0)
    stars = (255, 255, 20)

    RenderPointer = 0
    screen.fill(background)

    while True:
        try:
            neu = calc_primes([Bereich, Bereich + int(2200 + len(Primzahlen)*5)])
            for i in neu:
                if i not in Primzahlen:
                    Primzahlen.append(i)
            Bereich += 220
        except:
            pass

        Buffer = RenderPointer
        while RenderPointer < Buffer + 2200 and RenderPointer < len(Primzahlen):
            c = get_cords(Primzahlen[RenderPointer], Zoom)
            pygame.draw.rect(screen, stars, (c[0] + 1920, c[1] + 1080, 1, 1))
            pygame.display.update()
            RenderPointer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print(Zoom)
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    Zoom /= 1.5
                    screen.fill(background)
                    RenderPointer = 0
                elif event.key == pygame.K_m:
                    Zoom *= 1.5
                    screen.fill(background)
                    RenderPointer = 0
                elif event.key == pygame.K_PLUS:
                    Zoom /= 1.1
                    screen.fill(background)
                    RenderPointer = 0
                elif event.key == pygame.K_MINUS:
                    Zoom *= 1.1
                    screen.fill(background)
                    RenderPointer = 0
