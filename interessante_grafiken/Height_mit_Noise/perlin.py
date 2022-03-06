import random
from heigtmap_neu import render_heightmap
import Perlin_Lib
from heigtmap_neu import make_png
from multiprocessing import Pool
from functools import partial
from PIL import Image


def make_island_png(karte, file):
    karte = remake_map(karte)
    for i in range(len(karte)):
        for j in range(len(karte[i])):
            karte[i][j] = get_color(karte[i][j])
    fertig = karte.copy()
    del karte
    alles = [fertig[i][j] for i in range(len(fertig)) for j in range(len(fertig[i]))]
    img = Image.new('RGB', (len(fertig), len(fertig[0])))
    img.putdata(alles)
    img.save(file)
    print('Die Datei "' + file + '" wurde erstellt.')


def get_color(height):
    farben = [[(0, 0, 0), -10.1], [(0, 100, 0), 0], [(0, 255, 0), 10.1]]
    if type(height) == tuple:  # wurde bereits gemacht
        return height
    rgb = [0, 0, 0]
    for k in range(len(farben)):
        if farben[k][1] > height:
            if k == 0:
                return farben[k][0]
            else:
                for l in range(len(rgb)):
                    delta_y = farben[k - 1][0][l] - farben[k][0][l]
                    delta_x = farben[k - 1][1] - farben[k][1]
                    x3 = height
                    x1 = farben[k - 1][1]
                    y1 = farben[k - 1][0][l]

                    rgb[l] = int(((delta_y/delta_x) * (x3 - x1)) + y1)
                return tuple(rgb)
    return (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))


def get_noise(y, size, scale, p):
    result = [p.two(x * scale, y * scale) for x in range(size)]
    result.append(y)
    return result


def get_heightmap(size, scale, seed):
    perlin = Perlin_Lib.perlin(seed)
    p = Pool()

    # TODO: nicht für jede Zeile einen Prozess erzeugen, sondern nur insgesamt 12
    y = range(size)
    size -= 1
    func = partial(get_noise, size=size, scale=scale, p=perlin)
    result = p.map(func, iterable=y)
    p.close()
    p.join()
    return result


def show_karte(karte):
    '''for i in range(len(karte)):
        print(karte[i])
    print('------')'''
    pass


def remake_map(karte):
    buffer = [karte[i][j] for i in range(len(karte)) for j in range(len(karte[i]))]

    if max(buffer) != 0:
        scale = 20 / max(buffer)

        for i in range(len(karte)):
            for j in range(len(karte)):
                karte[i][j] *= scale
                karte[i][j] -= 10
    show_karte(karte)
    return karte


if __name__ == '__main__':
    X = 10
    Y = 10
    Size = 20003
    Seed = random.randrange(0, 70)
    f = open('seed.txt', 'w')
    f.write(str(Seed))
    f.close()
    Karte = get_heightmap(Size, 1, random.randrange(0, 70))
    # Karte = [[(x + y)//200 for x in range(X)] for y in range(Y)]
    # Karte = remake_map(Karte)
    # render_heightmap(Karte)

    make_png(Karte, 'perlin_test.png')
    make_island_png(Karte.copy(), 'Insel.png')

