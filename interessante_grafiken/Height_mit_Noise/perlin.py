import random
from heigtmap_neu import render_heightmap
import Perlin_Lib
from heigtmap_neu import make_png
from multiprocessing import Pool
from functools import partial
from PIL import Image


def make_island_png(karte, file):
    farben = [[(30, 144, 255), -10], [(255, 255, 255), 10]]

    for i in range(len(karte)):
        for j in range(len(karte)):
            for k in range(len(farben)):
                print(karte[i][j<])
                if karte[i][j] < farben[k][1]:
                    if k != 0:
                        rgb = [0, 0, 0]
                        for l in range(3):
                            farbdiff = farben[k][0][l] - farben[k-1][0][l]
                            heightdiff = farben[k][1] - farben[k-1][1]
                            real_heightdiff = farben[k][1] - karte[i][j]
                            scale = real_heightdiff / heightdiff
                            scale *= farbdiff
                            rgb[l] = farben[k][0][l] + scale
                    else:
                        karte[i][j] = farben[0][0]
            karte[i][j] = (rgb[0], rgb[1], rgb[2])

    fertig = karte.copy()
    alles = [fertig[i][j] for i in range(len(fertig)) for j in range(len(fertig))]
    img = Image.new('RGB', (len(fertig), len(fertig)))
    img.putdata(alles)
    img.save(file)
    print('Die Datei "' + file + '" wurde erstellt.')


def get_noise(y, size, scale, p):
    result = [p.two(x * scale, y * scale) for x in range(size)]
    result.append(y)
    return result


def get_heightmap(size, scale, seed):
    perlin = Perlin_Lib.perlin(seed)
    p = Pool()

    y = range(size)
    func = partial(get_noise, size=size, scale=scale, p=perlin)
    result = p.map(func, iterable=y)
    p.close()
    p.join()
    return result


def show_karte(karte):
    for i in range(len(karte)):
        print(karte[i])


def remake_map(karte):
    buffer = [karte[i][j] for i in range(len(karte)) for j in range(len(karte))]

    if max(buffer) != 0:
        scale = 20 / max(buffer)
    else:
        scale = 1

        for i in range(len(karte)):
            for j in range(len(karte)):
                karte[i][j] *= scale
                karte[i][j] -= 10
    return karte


if __name__ == '__main__':
    Karte = get_heightmap(500, 1, random.randrange(0, 70))
    render_heightmap(Karte)
    Karte = remake_map(Karte)
    make_island_png(Karte, 'Insel.png')
    make_png(Karte, 'perlin_test.png')

