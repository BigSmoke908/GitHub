from numba import jit, cuda
import time
from multiprocessing import Pool


# @jit(target='cuda')
def eins(zeug):
    for i in range(len(zeug)):
        zeug[i] += 1
    return 0


if __name__ == '__main__':
    anzahl = 429981696
    testdata = [200 for i in range(anzahl)]
    print('Normal auf der CPU')
    begin = time.time()
    alles = eins(testdata)
    print('Dauer auf der CPU (SingleCore): ' + str(time.time() - begin), '\n')

    testdata = [[200 for i in range(anzahl // 12)] for j in range(12)]
    print('Multiprocessing auf der CPU')
    begin = time.time()
    p = Pool()
    alles = p.map(func=eins, iterable=testdata)
    print('Dauer auf der CPU (MultiCore): ' + str(time.time() - begin), '\n')
