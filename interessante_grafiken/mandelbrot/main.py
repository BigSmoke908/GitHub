import pygame
import sys
from PIL import Image
from multiprocessing import Pool
from functools import partial


def avg(liste):
    return sum(liste)/len(liste)


def mandelbrot(re, im, max_iter):
    c = complex(re, im)
    z = 0.0j

    for i in range(max_iter):
        z = z ** 2 + c
        neu = z.real ** 2 + z.imag ** 2
        if neu >= 4:
            color = i * (255 / max_iter)
            return int((color / 1.8) + 50), int((color / 1.6) + 20), int((color / 1.4)), 0
    return abs(int(50 * z.real)), abs(int(50 * z.real)), abs(int(50 * z.real)), abs(int(50 * z.real))


# guckt ob ein bestimmter Wert Teil von dem Mandelbrotset ist -> wenn nein -> gibt den Pfad zurück (für Buddhabrot)
def test_mandelbrot(re, im, max_iterations):
    c = complex(re, im)
    z = 0.0j

    pfad = []

    for iterationen in range(max_iterations):
        z = z ** 2 + c
        pfad.append([z.real, z.imag, z])
        if z.real ** 2 + z.imag ** 2 >= 4:
            return pfad
    return []


def buddhabrot_single_thread(abschnitt1, max_iterations, file='b_set.png', make_file=True, abschnitt2=(0, 3840)):
    b_set = [[0 for x in range(3840)] for y in range(2160)]

    for i in range(abschnitt1[0], abschnitt1[1]):
        for j in range(abschnitt2[0], abschnitt2[1]):
            abschnitt = test_mandelbrot((i/540)-2.4, (j/540)-3.5, max_iterations)

            if len(abschnitt) != 0:
                for punkt in abschnitt:
                    try:
                        b_set[int((punkt[0]+2.4)*540)][int((punkt[1]+3.5)*540)] += 1
                    except:
                        pass
        if i % 100 == 0:
            print('a')

    if make_file:
        scale = 255/maxima(b_set)
        bild = []
        for zeile in range(len(b_set)):
            for spalte in range(len(b_set[zeile])):
                try:
                    farbe = int(b_set[zeile][spalte] * scale)
                    farbe = (farbe, farbe, farbe)
                    bild.append(farbe)
                except Exception as e:
                    print(e)
                    print(b_set[zeile][spalte], scale)
                    sys.exit('You are an Idiot :)')
        img = Image.new('RGB', (3840, 2160))
        img.putdata(bild)
        img.save(file)
    return b_set


def verteile_aufgaben(bereich, anzahl=11):
    return [[i, i + (bereich[1] - bereich[0])//anzahl, i//((bereich[1] - bereich[0])//anzahl)] for i in range(bereich[0], bereich[1], (bereich[1] - bereich[0])//anzahl)]


def buddhabrot_multi_threads(max_iterations, file='b_set.png'):
    p = Pool()
    alle_sets = [[0 for x in range(3840)] for y in range(2160)]

    function = partial(buddhabrot_single_thread, max_iterations=max_iterations, make_file=False)
    results = p.map(function, iterable=verteile_aufgaben([0, 2160], 12))

    for zeile in range(len(alle_sets)):
        for reihe in range(len(alle_sets[zeile])):
            for ergebnis in range(len(results)):
                alle_sets[zeile][reihe] += results[ergebnis][zeile][reihe]

    scale = 255/maxima(alle_sets)
    bild = []

    for x in range(len(alle_sets)):
        for y in range(len(alle_sets[x])):
            farbe = int(alle_sets[x][y] * scale)
            farbe = (farbe, farbe, farbe)
            bild.append(farbe)

    img = Image.new('RGB', (3840, 2160))
    img.putdata(bild)
    img.save(file)
    print('Sucess!')
    return alle_sets


def maxima(eingabe):
    return max([max(liste) for liste in eingabe])


counter = 0
alles = []
normal_Mandelbrot = False
if normal_Mandelbrot:
    pygame.init()
    screen = pygame.display.set_mode((2000, 2000))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(screen, 'mandelbrot.png')
                pygame.quit()
                print(max(alles))
                sys.exit()

        if counter <= 2000:
            for i in range(counter, counter + 50):
                for j in range(2000):
                    farbe = mandelbrot((i - 1200) / 500, (j - 1000) / 500, 500)
                    alles.append(farbe[3])
                    try:
                        pygame.draw.rect(screen, (farbe[0], farbe[1], farbe[2]), (i, j, 1, 1))
                    except:
                        print(farbe)
                        sys.exit()
        counter += 50
        pygame.display.update()


if __name__ == '__main__':
    buddhabrot_multi_threads(10000)
