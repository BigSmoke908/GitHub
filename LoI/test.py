import math

def feld_zeichnen(feld):
    for i in range(len(feld)):
        buffer = ''
        for j in range(len(feld[i])):
                       buffer += str(feld[i][j])
        print(buffer)



#  den Punkt raussuchen wo die Spirale anfängt
def finde_mitte(feld):
    x = len(feld)/2

    if type(x) != int:
        x = (x//2) + 1

    y = len(feld[0])/2

    if type(x) != int:
        y = (y//2) + 1

    return y, x


def erzeuge_spirale(maximum, y, x, spirale):
    print(x, y)
    spirale[y][x] = 1
    x += 1
    spirale[y][x] = 2
    for i in range(3, maximum):
        if spirale[y][x - 1] != 0 and spirale[y - 1][x - 1] != 0 and spirale[y - 1][x] == 0:  # es muss nach oben gegangen werden
            spirale[y - 1][x] = i
            y -= 1
        elif spirale[y + 1][x] != 0 and spirale[y + 1][x + 1] != 0 and spirale[y][x - 1] == 0:  # es muss nach links gegangen werden
            spirale[y][x - 1] = i
            x -= 1
        elif spirale[y][x + 1] != 0 and spirale[y + 1][x + 1] != 0 and spirale[y + 1][x] == 0:  # es muss nach unten gegangen werden
            spirale[y + 1][x] = i
            y += 1
        elif spirale[y - 1][x] != 0 and spirale[y - 1][x + 1] != 0 and spirale[y][x + 1] == 0:
            spirale[y][x + 1] = i
            x += 1
        else:
            print('ein seltsamer Fehler ist aufgetreten')
        feld_zeichnen(spirale)
    return spirale
            

spirale = {}


print('gib die Spiralenlänge ein!')
maximum = input()
# maximum = maximum ** 2


try:
    maximum = int(maximum)
except:
    print('Die Eingabe "' + str(maximum) + '" ist falsch')


for i in range(maximum):
    spirale[i] = []


for i in range(len(spirale)):
    for j in range(maximum):
        spirale[i].append(0)


x, y = finde_mitte(spirale)
spirale = erzeuge_spirale(maximum, int(y), int(x), spirale)
