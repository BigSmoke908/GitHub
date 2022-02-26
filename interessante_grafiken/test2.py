import time
from multiprocessing import Pool
from functools import partial


def intensive_calc(i, x):
    neu = [j for j in range(x)]
    pool = Pool()

    funcs = partial(intensive_calc_neu, i=i)
    resultat = pool.map(funcs, iterable=neu)

    return resultat


def intensive_calc_neu(i, x):
    anfang = time.time()
    while time.time() - 1 < anfang:
        x *= x
    return i


if __name__ == '__main__':
    begin = time.time()
    numbers = [i for i in range(100)]
    p = Pool()

    func = partial(intensive_calc, x=2)
    result = p.map(func, iterable=numbers)
    print(result)

    p.close()
    p.join()

    print('Rechenzeit = ' + str(time.time() - begin))

    begin = time.time()

    result = []
    for i in numbers:
        result.append(intensive_calc(i, 2))
    print(result)
    print('Rechenzeit = ' + str(time.time() - begin))
